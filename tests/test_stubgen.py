import os
from unittest.mock import MagicMock, patch

from wg.core.stubgen import (
    DEFAULT_GAME_VERSION,
    _resolve_application_id,
    fetch_game_version,
    get_bundled_spec_path,
    get_default_storage_path,
    get_default_stub_path,
)


def test_resolve_application_id_direct():
    assert _resolve_application_id("test_app_id") == "test_app_id"


@patch.dict(os.environ, {"WG_APP_ID": "env_app_id"})
def test_resolve_application_id_env():
    assert _resolve_application_id() == "env_app_id"


@patch("wg.core.stubgen.Path.exists")
@patch("wg.core.stubgen.Path.read_text")
def test_resolve_application_id_secrets(mock_read, mock_exists):
    mock_exists.return_value = True
    mock_read.return_value = "secret_app_id\n"
    with patch.dict(os.environ, {}, clear=True):
        assert _resolve_application_id() == "secret_app_id"


@patch("sys.platform", "linux")
@patch.dict(os.environ, {"XDG_CACHE_HOME": "/custom/cache"})
def test_get_default_storage_path_xdg():
    path = get_default_storage_path()
    assert str(path) == "/custom/cache/wg/wows"


@patch("sys.platform", "win32")
@patch.dict(os.environ, {"LOCALAPPDATA": "C:\\Users\\test\\AppData\\Local"})
def test_get_default_storage_path_win32():
    path = get_default_storage_path()
    assert path.parts[-2:] == ("wg", "wows")


@patch("sys.platform", "darwin")
def test_get_default_storage_path_darwin():
    path = get_default_storage_path()
    assert str(path).endswith("Library/Caches/wg/wows")


def test_get_bundled_spec_path():
    path = get_bundled_spec_path("wows")
    assert path.name == "wows_api_spec.json"
    assert "data" in path.parts


def test_get_default_stub_path():
    path = get_default_stub_path("wows")
    assert path.name == "client.pyi"


@patch("urllib.request.urlopen")
def test_fetch_game_version_success(mock_urlopen):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'{"status": "ok", "data": {"game_version": "1.2.3"}}'
    mock_urlopen.return_value.__enter__.return_value = mock_response

    version = fetch_game_version(application_id="test")
    assert version == "1.2.3"


@patch("urllib.request.urlopen")
def test_fetch_game_version_api_error(mock_urlopen):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'{"status": "error", "error": {"message": "INVALID_APP_ID"}}'
    mock_urlopen.return_value.__enter__.return_value = mock_response

    version = fetch_game_version(application_id="test")
    assert version == DEFAULT_GAME_VERSION


@patch("urllib.request.urlopen")
def test_fetch_game_version_exception(mock_urlopen):
    mock_urlopen.side_effect = Exception("Network error")
    version = fetch_game_version(application_id="test")
    assert version == DEFAULT_GAME_VERSION


def test_fetch_game_version_no_app_id():
    with patch("wg.core.stubgen._resolve_application_id", return_value=None):
        version = fetch_game_version()
        assert version == DEFAULT_GAME_VERSION
