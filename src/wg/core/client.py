import logging
from pathlib import Path
from typing import Any, Callable, Dict, cast

import aiohttp

from ._stubgen import ensure_type_stubs, get_default_storage_path, load_or_fetch_spec

logger = logging.getLogger(__name__)


def _wrap_dict_or_list(data: Any) -> Any:
    """Recursively wrap dicts into AttrDict and recurse into lists."""
    if isinstance(data, dict):
        return AttrDict(data)
    elif isinstance(data, list):
        return [_wrap_dict_or_list(item) for item in data]
    return data


class AttrDict(dict):
    """Dictionary subclass that allows attribute-style access to keys."""

    def __init__(self, mapping=None, **kwargs):
        super().__init__()
        if mapping:
            for key, value in mapping.items():
                self[key] = _wrap_dict_or_list(value)
        if kwargs:
            for key, value in kwargs.items():
                self[key] = _wrap_dict_or_list(value)

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            if isinstance(item, int) and str(item) in self:
                return super().__getitem__(str(item))
            if isinstance(item, str) and item.isdigit() and int(item) in self:
                return super().__getitem__(int(item))
            raise

    def get(self, item, default=None):
        try:
            return self[item]
        except KeyError:
            return default

    def __contains__(self, item):
        if super().__contains__(item):
            return True
        if isinstance(item, int) and str(item) in self:
            return True
        if isinstance(item, str) and item.isdigit() and int(item) in self:
            return True
        return False

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            stats = super().get("statistics")
            if isinstance(stats, dict) and item in stats:
                return stats[item]
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{item}'"
            ) from None

    def __setattr__(self, key, value):
        self[key] = _wrap_dict_or_list(value)


class BaseWargamingAPIClient:
    def __init__(
        self,
        application_id: str,
        game_title: str,
        api_domain: str,
        base_urls: dict[str, str],
        storage_path: str | Path | None = None,
        logger: logging.Logger | None = None,
        stub_path: str | Path | None = None,
    ):
        self.application_id = application_id
        self.game_title = game_title
        self.api_domain = api_domain
        self.base_urls = base_urls
        self.storage_path = (
            Path(storage_path) if storage_path else get_default_storage_path(self.game_title)
        )
        self.logger = logger or logging.getLogger(__name__)
        self.stub_path = Path(stub_path) if stub_path else None

        self._load_dynamic_methods()

    def _load_dynamic_methods(self):
        try:
            spec_data = load_or_fetch_spec(
                storage_path=self.storage_path,
                log=self.logger,
                api_domain=self.api_domain,
                game_title=self.game_title,
            )

            for method_info in spec_data.get("methods", []):
                method_key = method_info.get("method_key")
                if not method_key:
                    continue
                endpoint = f"/{self.game_title}/{method_info['url']}/"

                # Create a closure for the dynamic method
                def create_api_method(ep, name, desc) -> Callable:
                    async def api_method(region: str, **kwargs) -> Dict[str, Any]:
                        return await self._request(region, ep, kwargs)

                    api_method.__name__ = name
                    api_method.__doc__ = desc
                    return api_method

                setattr(
                    self,
                    method_key,
                    create_api_method(endpoint, method_key, method_info.get("description", "")),
                )

            # Automatically ensure type stubs exist for IDE support
            ensure_type_stubs(
                spec_data=spec_data,
                stub_path=self.stub_path,
                storage_path=self.storage_path,
                application_id=self.application_id,
                log=self.logger,
                api_domain=self.api_domain,
                game_title=self.game_title,
            )

        except Exception as e:
            self.logger.error(f"Failed to load dynamic methods from spec: {e}")

    def _get_base_url(self, region: str) -> str:
        url = self.base_urls.get(region.lower())
        if not url:
            raise ValueError(f"Unsupported region: {region}")
        return url

    async def _request(self, region: str, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        base_url = self._get_base_url(region)
        url = f"{base_url}{endpoint}"
        params["application_id"] = self.application_id

        logger = self.logger

        # Convert lists to comma-separated strings for WG API
        processed_params = {}
        for k, v in params.items():
            if isinstance(v, list):
                processed_params[k] = ",".join(map(str, v))
            elif v is not None:
                processed_params[k] = v

        logger.debug(f"Request: {url} | Params: {processed_params}")

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=processed_params) as resp:
                if resp.status != 200:
                    logger.error(f"WG API error {resp.status} for {url}")
                    raise Exception(f"WG API error {resp.status}")
                data = await resp.json()
                logger.debug(f"Response from {endpoint}: {data}")
                if data.get("status") != "ok":
                    logger.error(f"WG API error: {data.get('error')}")
                    raise Exception(f"WG API error: {data.get('error')}")

                # Wrap the data in AttrDict/lists so dot access works
                wrapped_data = _wrap_dict_or_list(data.get("data", {}))
                return cast(Dict[str, Any], wrapped_data)
