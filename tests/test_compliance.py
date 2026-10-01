import io
import zipfile
from pathlib import Path

import pytest
from wg.compliance import extract_deleted_account_ids


@pytest.fixture
def sample_csv_content():
    return b"account_id\n12345\n67890\n"


@pytest.fixture
def sample_csv_no_header_content():
    return b"12345\n67890\n"


@pytest.fixture
def sample_zip_path(tmp_path, sample_csv_content):
    zip_path = tmp_path / "deleted_accounts.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("accounts.csv", sample_csv_content)
    return zip_path


@pytest.fixture
def sample_csv_path(tmp_path, sample_csv_content):
    csv_path = tmp_path / "accounts.csv"
    csv_path.write_bytes(sample_csv_content)
    return csv_path


def test_extract_from_zip_path(sample_zip_path):
    ids = list(extract_deleted_account_ids(sample_zip_path))
    assert ids == [12345, 67890]


def test_extract_from_csv_path(sample_csv_path):
    ids = list(extract_deleted_account_ids(sample_csv_path))
    assert ids == [12345, 67890]


def test_extract_from_zip_bytes(sample_csv_content):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("accounts.csv", sample_csv_content)
    buf.seek(0)

    ids = list(extract_deleted_account_ids(buf.read()))
    assert ids == [12345, 67890]


def test_extract_from_csv_bytes(sample_csv_content):
    ids = list(extract_deleted_account_ids(sample_csv_content))
    assert ids == [12345, 67890]


def test_extract_from_csv_bytes_no_header(sample_csv_no_header_content):
    ids = list(extract_deleted_account_ids(sample_csv_no_header_content))
    assert ids == [12345, 67890]


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        list(extract_deleted_account_ids(Path("nonexistent.zip")))


def test_invalid_type():
    with pytest.raises(TypeError):
        list(extract_deleted_account_ids(123))  # type: ignore
