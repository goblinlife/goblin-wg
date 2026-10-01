from unittest.mock import AsyncMock, patch

import pytest
from wg.core.client import AttrDict, _wrap_dict_or_list
from wg.wot.client import WargamingAPIClient as WotClient
from wg.wows.client import WargamingAPIClient as WowsClient


def test_wrap_dict_or_list():
    data = {"a": 1, "b": [{"c": 2}, 3]}
    wrapped = _wrap_dict_or_list(data)
    assert isinstance(wrapped, AttrDict)
    assert wrapped.a == 1
    assert isinstance(wrapped.b, list)
    assert isinstance(wrapped.b[0], AttrDict)
    assert wrapped.b[0].c == 2
    assert wrapped.b[1] == 3


def test_attr_dict():
    d = AttrDict({"foo": "bar", "num": 42}, extra="value")
    assert d.foo == "bar"
    assert d.num == 42
    assert d.extra == "value"
    assert d["foo"] == "bar"

    # Test int key access
    d["123"] = "numeric_str"
    assert d[123] == "numeric_str"  # pyright: ignore[reportArgumentType]
    assert d["123"] == "numeric_str"

    d[456] = "numeric_int"  # pyright: ignore[reportArgumentType]
    assert d[456] == "numeric_int"  # pyright: ignore[reportArgumentType]
    assert d["456"] == "numeric_int"

    # Test nested statistics fallback
    d["statistics"] = {"pvp": {"battles": 10}}
    assert d.pvp["battles"] == 10

    with pytest.raises(AttributeError):
        _ = d.nonexistent


@pytest.mark.parametrize(
    "ClientClass, expected_url",
    [
        (WowsClient, "https://api.worldofwarships.com"),
        (WotClient, "https://api.worldoftanks.com"),
    ],
)
@patch("wg.core.client.load_or_fetch_spec")
@patch("wg.core.client.ensure_type_stubs")
def test_wargaming_api_client_init(mock_ensure, mock_load, ClientClass, expected_url):
    mock_load.return_value = {
        "methods": [
            {
                "method_key": "account_list",
                "url": "account/list",
                "description": "List accounts",
            }
        ]
    }

    client = ClientClass("test_app_id")
    assert client.application_id == "test_app_id"
    assert hasattr(client, "account_list")

    assert client._get_base_url("na") == expected_url
    with pytest.raises(ValueError, match="Unsupported region: invalid"):
        client._get_base_url("invalid")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ClientClass",
    [WowsClient, WotClient],
)
@patch("wg.core.client.load_or_fetch_spec")
@patch("wg.core.client.ensure_type_stubs")
@patch("aiohttp.ClientSession.get")
async def test_wargaming_api_client_request(mock_get, mock_ensure, mock_load, ClientClass):
    mock_load.return_value = {
        "methods": [
            {
                "method_key": "account_list",
                "url": "account/list",
            }
        ]
    }

    client = ClientClass("test_app_id")

    # Mock response
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {"status": "ok", "data": {"12345": {"nickname": "player"}}}

    # Setup context manager for session.get
    mock_get.return_value.__aenter__.return_value = mock_response

    endpoint = f"/{client.game_title}/account/list/"
    result = await client._request(
        "na", endpoint, {"search": "player", "fields": ["account_id", "nickname"]}
    )

    assert isinstance(result, AttrDict)
    assert result["12345"].nickname == "player"

    # Verify aiohttp was called correctly with params parsed
    mock_get.assert_called_once()
    called_url, called_kwargs = mock_get.call_args
    assert called_url[0] == f"{client._get_base_url('na')}{endpoint}"
    assert called_kwargs["params"] == {
        "search": "player",
        "fields": "account_id,nickname",
        "application_id": "test_app_id",
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ClientClass",
    [WowsClient, WotClient],
)
@patch("wg.core.client.load_or_fetch_spec")
@patch("wg.core.client.ensure_type_stubs")
@patch("aiohttp.ClientSession.get")
async def test_wargaming_api_client_request_error(mock_get, mock_ensure, mock_load, ClientClass):
    mock_load.return_value = {}
    client = ClientClass("test_app_id")

    mock_response = AsyncMock()
    mock_response.status = 500
    mock_get.return_value.__aenter__.return_value = mock_response

    with pytest.raises(Exception, match="WG API error 500"):
        await client._request("na", "/test/", {})

    mock_response.status = 200
    mock_response.json.return_value = {"status": "error", "error": "INVALID_APPLICATION_ID"}

    with pytest.raises(Exception, match="WG API error: INVALID_APPLICATION_ID"):
        await client._request("na", "/test/", {})
