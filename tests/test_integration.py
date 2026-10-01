import os
from pathlib import Path

import pytest
from wg.wot.client import WargamingAPIClient as WotClient
from wg.wows.client import WargamingAPIClient as WowsClient


def get_app_id() -> str | None:
    app_id = os.environ.get("WG_APP_ID")
    if app_id:
        return app_id

    env_path = Path(__file__).parent.parent.parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("WG_APP_ID="):
                return line.split("=", 1)[1].strip()
    return None


APP_ID = get_app_id()

pytestmark = pytest.mark.skipif(
    not APP_ID, reason="WG_APP_ID not found in environment or .env file"
)


@pytest.mark.asyncio
async def test_wows_integration_account_list():
    # Arrange
    client = WowsClient(application_id=APP_ID)  # type: ignore

    # Act
    res = await client.wows_account_list(region="na", search="dev", limit=3)

    # Assert
    assert isinstance(res, list)
    assert len(res) <= 3
    if len(res) > 0:
        assert hasattr(res[0], "account_id")
        assert hasattr(res[0], "nickname")


@pytest.mark.asyncio
async def test_wot_integration_account_list():
    # Arrange
    client = WotClient(application_id=APP_ID)  # type: ignore

    # Act
    res = await client.wot_account_list(region="na", search="dev", limit=3)

    # Assert
    assert isinstance(res, list)
    assert len(res) <= 3
    if len(res) > 0:
        assert hasattr(res[0], "account_id")
        assert hasattr(res[0], "nickname")
