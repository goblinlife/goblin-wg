import argparse
from unittest.mock import patch

from wg.main import (
    _cmd_title_fetch_spec,
    _cmd_title_generate_stubs,
    _cmd_title_info,
    _dispatch_compliance,
)


@patch("wg.main.generate_type_stubs")
def test_cmd_wows_generate_stubs(mock_generate, tmp_path):
    out_path = tmp_path / "client.pyi"
    args = argparse.Namespace(
        title="wows", output=out_path, force=True, storage_path=tmp_path, application_id="test"
    )
    assert _cmd_title_generate_stubs(args) == 0
    mock_generate.assert_called_once()


@patch("wg.main.fetch_remote_spec")
@patch("wg.main.generate_type_stubs")
def test_cmd_wows_fetch_spec(mock_generate, mock_fetch, tmp_path):
    mock_fetch.return_value = {"_meta": {"api_version": "1.0"}}
    args = argparse.Namespace(title="wows", storage_path=tmp_path, generate_stubs=True, application_id="test")
    assert _cmd_title_fetch_spec(args) == 0
    mock_fetch.assert_called_once()
    mock_generate.assert_called_once()


@patch("wg.main.fetch_remote_spec")
def test_cmd_wows_fetch_spec_no_stubs(mock_fetch, tmp_path):
    mock_fetch.return_value = {"_meta": {"api_version": "1.0"}}
    args = argparse.Namespace(title="wows", storage_path=tmp_path, generate_stubs=False, application_id="test")
    assert _cmd_title_fetch_spec(args) == 0
    mock_fetch.assert_called_once()


@patch("wg.main.fetch_remote_spec")
def test_cmd_wows_fetch_spec_fail(mock_fetch, tmp_path):
    mock_fetch.return_value = None
    args = argparse.Namespace(title="wows", storage_path=tmp_path, generate_stubs=False, application_id="test")
    assert _cmd_title_fetch_spec(args) == 1


@patch("wg.main.get_default_stub_path")
def test_cmd_wows_info(mock_get_stub_path, tmp_path):
    mock_get_stub_path.return_value = tmp_path / "client.pyi"
    spec_path = tmp_path / "wows_api_spec.json"
    spec_path.write_text('{"_meta": {"api_version": "1.0"}, "methods": []}')
    args = argparse.Namespace(title="wows", storage_path=tmp_path)
    assert _cmd_title_info(args) == 0


@patch("wg.compliance.extract_deleted_account_ids")
def test_dispatch_compliance(mock_extract, tmp_path):
    mock_extract.return_value = iter([123, 456])
    args = argparse.Namespace(
        compliance_command="extract-deleted", file=tmp_path / "test.zip", format="json"
    )

    assert _dispatch_compliance(args) == 0

    args.format = "csv"
    assert _dispatch_compliance(args) == 0

    args.format = "text"
    assert _dispatch_compliance(args) == 0
