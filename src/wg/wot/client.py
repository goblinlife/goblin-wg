import logging
from pathlib import Path

from wg.core.client import BaseWargamingAPIClient


class WargamingAPIClient(BaseWargamingAPIClient):
    def __init__(
        self,
        application_id: str,
        storage_path: str | Path | None = None,
        logger: logging.Logger | None = None,
    ):
        base_urls = {
            "na": "https://api.worldoftanks.com",
            "eu": "https://api.worldoftanks.eu",
            "asia": "https://api.worldoftanks.asia",
            "ru": "https://api.worldoftanks.ru",
        }
        stub_path = Path(__file__).parent / "client.pyi"
        super().__init__(
            application_id=application_id,
            game_title="wot",
            api_domain="api.worldoftanks.com",
            base_urls=base_urls,
            storage_path=storage_path,
            logger=logger,
            stub_path=stub_path,
        )
