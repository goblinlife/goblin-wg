import csv
import io
import zipfile
from pathlib import Path
from typing import Iterator


def extract_deleted_account_ids(file_path: Path | str | bytes) -> Iterator[int]:
    """
    Reads a Wargaming 'deleted_accounts.zip' (or raw 'accounts.csv')
    and yields the account IDs to be deleted.
    """
    if isinstance(file_path, (str, Path)):
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path, 'r') as zf:
                if 'accounts.csv' not in zf.namelist():
                    raise ValueError("accounts.csv not found in the zip file.")

                with zf.open('accounts.csv') as f:
                    yield from _parse_csv(io.TextIOWrapper(f, encoding='utf-8-sig'))
        else:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                yield from _parse_csv(f)
    elif isinstance(file_path, bytes):
        try:
            with zipfile.ZipFile(io.BytesIO(file_path), 'r') as zf:
                if 'accounts.csv' not in zf.namelist():
                    raise ValueError("accounts.csv not found in the zip file.")
                with zf.open('accounts.csv') as f:
                    yield from _parse_csv(io.TextIOWrapper(f, encoding='utf-8-sig'))
        except zipfile.BadZipFile:
            yield from _parse_csv(io.StringIO(file_path.decode('utf-8-sig')))
    else:
        raise TypeError("file_path must be a Path, str, or bytes.")

def _parse_csv(f) -> Iterator[int]:
    reader = csv.reader(f)
    header = next(reader, None)
    if not header:
        return

    if header[0].strip() != 'account_id':
        if header[0].strip().isdigit():
            yield int(header[0].strip())

    for row in reader:
        if row and row[0].strip().isdigit():
            yield int(row[0].strip())
