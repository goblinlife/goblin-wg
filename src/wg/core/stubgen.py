"""Private module for generating type stubs for Wargaming API clients."""

import json
import logging
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_GAME_VERSION = "15.8.0"


def _resolve_application_id(application_id: str | None = None) -> str | None:
    """Resolve WG application ID from argument, environment, or secrets file."""
    if application_id:
        return application_id
    env_id = os.environ.get("WG_APP_ID") or os.environ.get("WARGAMING_APPLICATION_ID")
    if env_id:
        return env_id
    secrets_path = Path("secrets/WG_APP_ID")
    if secrets_path.exists():
        try:
            val = secrets_path.read_text(encoding="utf-8").strip()
            if val:
                return val
        except OSError:
            pass
    return None


def fetch_game_version(
    application_id: str | None = None,
    log: logging.Logger | None = None,
    api_domain: str = "api.worldofwarships.com",
    game_title: str = "wows",
) -> str:
    """Fetch game client version from encyclopedia/info API endpoint."""
    current_logger = log or logger
    app_id = _resolve_application_id(application_id)
    if not app_id:
        current_logger.debug(
            "No application_id found for fetching game version; using default %s",
            DEFAULT_GAME_VERSION,
        )
        return DEFAULT_GAME_VERSION

    url = f"https://{api_domain}/{game_title}/encyclopedia/info/?application_id={app_id}&fields=game_version"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "goblin-wg-client"})
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                payload = json.loads(response.read().decode("utf-8"))
                if payload.get("status") == "ok":
                    game_ver = payload.get("data", {}).get("game_version")
                    if game_ver and isinstance(game_ver, str):
                        current_logger.debug("Fetched game version from API: %s", game_ver)
                        return game_ver
                else:
                    err_info = payload.get("error", {})
                    current_logger.warning(
                        "WG API error fetching game version: %s",
                        err_info.get("message", "Unknown error"),
                    )
    except Exception as err:
        current_logger.warning("Could not fetch game version from WG API: %s", err)

    return DEFAULT_GAME_VERSION


def get_default_storage_path(game_title: str = "wows") -> Path:
    """Return standard user cache directory for WG API data."""
    xdg = os.environ.get("XDG_CACHE_HOME")
    if xdg:
        return Path(xdg) / "wg" / game_title
    if sys.platform == "win32":
        appdata = os.environ.get("LOCALAPPDATA")
        base = Path(appdata) if appdata else Path.home() / "AppData" / "Local"
        return base / "wg" / game_title
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Caches" / "wg" / game_title
    return Path.home() / ".cache" / "wg" / game_title


def get_bundled_spec_path(game_title: str) -> Path:
    """Return path to fallback bundled spec file."""
    # We will assume data is adjacent to the caller, or we can look in wg/<game_title>/data
    return Path(__file__).parent.parent / game_title / "data" / f"{game_title}_api_spec.json"


def get_default_stub_path(game_title: str) -> Path:
    """Return path to client.pyi."""
    return Path(__file__).parent.parent / game_title / "client.pyi"


def _extract_enum_literal(help_text: str) -> str | None:
    """Extract enum values from field help text."""
    if "Valid values:" not in help_text:
        return None
    parts = help_text.split("Valid values:")
    if len(parts) <= 1:
        return None
    matches = re.findall(r'\*\s*"([^"]+)"', parts[1])
    if not matches:
        return None
    enum_str = ", ".join([f"'{m}'" for m in matches])
    return f"Literal[{enum_str}]"


def _resolve_field_type(field: dict[str, Any], literal_output_fields: str) -> str:
    """Resolve Python type annotation for a method parameter."""
    name = field.get("name")
    doc_type = field.get("doc_type", "")
    help_text = field.get("help_text", "")
    enum_literal = _extract_enum_literal(help_text)

    if name == "fields" and literal_output_fields:
        return f"Union[{literal_output_fields}, List[{literal_output_fields}], str]"
    if enum_literal:
        if "list" in doc_type:
            return f"Union[{enum_literal}, List[{enum_literal}]]"
        return enum_literal
    if "numeric" in doc_type and "list" in doc_type:
        return "Union[int, List[int], str]"
    if "string" in doc_type and "list" in doc_type:
        return "Union[str, List[str]]"
    if "numeric" in doc_type:
        return "int"
    if "string" in doc_type:
        return "str"
    return "Any"


def _build_method_args(method_info: dict[str, Any], literal_output_fields: str) -> list[str]:
    """Build argument list for a generated method signature."""
    args = ["self", "region: str"]
    req_fields: list[str] = []
    opt_fields: list[str] = []
    input_form = method_info.get("input_form_info") or {}
    fields = input_form.get("fields", [])

    for field in fields:
        name = field.get("name")
        if not name or name in ("application_id", "region"):
            continue
        py_type = _resolve_field_type(field, literal_output_fields)
        if field.get("required", False):
            req_fields.append(f"{name}: {py_type}")
        else:
            opt_fields.append(f"{name}: {py_type} = ...")

    args.extend(req_fields)
    args.extend(opt_fields)
    args.append("**kwargs")
    return args


def _format_method_signature(method_info: dict[str, Any]) -> list[str]:
    """Format single method signature with docstrings for the stub file."""
    method_key = method_info.get("method_key")
    if not method_key:
        return []

    output_form = method_info.get("output_form_info") or {}
    output_fields = [
        f.get("name")
        for f in output_form.get("fields", [])
        if f.get("name")
    ]
    literal_output_fields = (
        f"Literal[{', '.join([repr(f) for f in output_fields])}]" if output_fields else ""
    )

    args = _build_method_args(method_info, literal_output_fields)
    desc = method_info.get("description", "").replace("\n", "\n        ")

    lines = [f"    async def {method_key}({', '.join(args)}) -> Any:"]
    if desc:
        lines.append(f'        """\n        {desc}\n        """')
    lines.append("        ...")
    lines.append("")
    return lines


def _build_stub_header(
    spec_data: dict[str, Any],
    game_version: str | None = None,
) -> list[str]:
    """Construct header preamble and class definition for stub file."""
    meta = spec_data.get("_meta", {})
    resolved_game_ver = game_version or meta.get("game_version") or DEFAULT_GAME_VERSION
    fetch_date = meta.get("date", "Unknown")
    content_lang = meta.get("content_language", "Unknown")
    now = datetime.now().isoformat()

    return [
        '"""',
        "---",
        f"game_version: {resolved_game_ver}",
        f"updated_at: {now}",
        f"fetch_date: {fetch_date}",
        f"content_language: {content_lang}",
        "---",
        '"""',
        "# AUTO-GENERATED STUB FILE - DO NOT EDIT",
        "import logging",
        "from pathlib import Path",
        "from typing import Any, Dict, List, Literal, Optional, Union",
        "",
        "class AttrDict(dict[str, Any]):",
        "    def __init__(self, mapping: Optional[Dict[str, Any]] = ..., **kwargs: Any) -> None: ...",
        "    def __getattr__(self, item: str) -> Any: ...",
        "    def __setattr__(self, key: str, value: Any) -> None: ...",
        "",
        "class WargamingAPIClient:",
        "    application_id: str",
        "    storage_path: Path",
        "    base_urls: Dict[str, str]",
        "    def __init__(self, application_id: str, storage_path: str | Path | None = None, logger: logging.Logger | None = None) -> None: ...",
        "    def _get_base_url(self, region: str) -> str: ...",
        "    async def _request(self, region: str, endpoint: str, params: Dict[str, Any]) -> Any: ...",
        "",
    ]


def generate_stub_content(
    spec_data: dict[str, Any],
    game_version: str | None = None,
) -> str:
    """Generate complete string content for client.pyi."""
    lines = _build_stub_header(spec_data, game_version=game_version)
    for method_info in spec_data.get("methods", []):
        lines.extend(_format_method_signature(method_info))
    return "\n".join(lines)


def fetch_remote_spec(
    spec_path: Path | None = None,
    log: logging.Logger | None = None,
    api_domain: str = "api.worldofwarships.com",
    game_title: str = "wows",
) -> dict[str, Any] | None:
    """Fetch spec from Wargaming API with HTTP 304 handling."""
    current_logger = log or logger
    headers: dict[str, str] = {}
    if spec_path and spec_path.exists():
        mtime = spec_path.stat().st_mtime
        headers["If-Modified-Since"] = time.strftime(
            "%a, %d %b %Y %H:%M:%S GMT", time.gmtime(mtime)
        )

    try:
        req = urllib.request.Request(f"https://{api_domain}/{game_title}/", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                headers_dict = dict(response.headers)
                data["_meta"] = {
                    "api_version": headers_dict.get("X-Api-Version", "Unknown"),
                    "date": headers_dict.get("Date", "Unknown"),
                    "content_language": headers_dict.get("Content-Language", "Unknown"),
                }
                if spec_path:
                    try:
                        spec_path.parent.mkdir(parents=True, exist_ok=True)
                        spec_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
                        current_logger.info(f"Updated {game_title} API spec downloaded and saved.")
                    except OSError as err:
                        current_logger.warning("Could not write spec to %s: %s", spec_path, err)
                return data
    except urllib.error.HTTPError as err:
        if err.code == 304:
            current_logger.debug(f"{game_title} API spec is up to date (304 Not Modified).")
        else:
            current_logger.error(f"HTTP Error fetching {game_title} API spec: %s", err.code)
    except Exception as err:
        current_logger.error(f"Error fetching {game_title} API spec: %s", err)
    return None


def load_or_fetch_spec(
    storage_path: Path | None = None,
    log: logging.Logger | None = None,
    api_domain: str = "api.worldofwarships.com",
    game_title: str = "wows",
) -> dict[str, Any]:
    """Load cached spec, fetch remote updates, or fallback to bundled spec."""
    target_storage = storage_path or get_default_storage_path(game_title)
    spec_path = target_storage / f"{game_title}_api_spec.json"

    remote_spec = fetch_remote_spec(spec_path=spec_path, log=log, api_domain=api_domain, game_title=game_title)
    if remote_spec:
        return remote_spec

    if spec_path.exists():
        try:
            return json.loads(spec_path.read_text(encoding="utf-8"))
        except Exception as err:
            (log or logger).warning("Failed to parse cached spec at %s: %s", spec_path, err)

    bundled_path = get_bundled_spec_path(game_title)
    if bundled_path.exists():
        try:
            return json.loads(bundled_path.read_text(encoding="utf-8"))
        except Exception as err:
            (log or logger).warning("Failed to parse bundled spec at %s: %s", bundled_path, err)

    raise RuntimeError(
        f"Could not load {game_title} API spec from network, cache, or bundled fallback."
    )


def generate_type_stubs(
    spec_data: dict[str, Any] | None = None,
    stub_path: Path | None = None,
    storage_path: Path | None = None,
    application_id: str | None = None,
    log: logging.Logger | None = None,
    api_domain: str = "api.worldofwarships.com",
    game_title: str = "wows",
) -> Path:
    """Generate client.pyi type stubs file."""
    current_logger = log or logger
    target_stub_path = stub_path or get_default_stub_path(game_title)

    if spec_data is None:
        spec_data = load_or_fetch_spec(
            storage_path=storage_path, log=current_logger, api_domain=api_domain, game_title=game_title
        )

    game_version = fetch_game_version(
        application_id=application_id, log=current_logger, api_domain=api_domain, game_title=game_title
    )
    content = generate_stub_content(spec_data, game_version=game_version)
    try:
        target_stub_path.parent.mkdir(parents=True, exist_ok=True)
        target_stub_path.write_text(content, encoding="utf-8")
        current_logger.debug("Successfully generated type stubs at %s", target_stub_path)
    except PermissionError:
        current_logger.warning(
            "Permission denied writing stubs to %s. Stub file was not updated.",
            target_stub_path,
        )
    return target_stub_path


def ensure_type_stubs(
    spec_data: dict[str, Any] | None = None,
    stub_path: Path | None = None,
    storage_path: Path | None = None,
    application_id: str | None = None,
    log: logging.Logger | None = None,
    api_domain: str = "api.worldofwarships.com",
    game_title: str = "wows",
) -> Path:
    """Ensure client.pyi exists; generate it if missing."""
    target_stub_path = stub_path or get_default_stub_path(game_title)
    if not target_stub_path.exists():
        return generate_type_stubs(
            spec_data=spec_data,
            stub_path=target_stub_path,
            storage_path=storage_path,
            application_id=application_id,
            log=log,
            api_domain=api_domain,
            game_title=game_title,
        )
    return target_stub_path
