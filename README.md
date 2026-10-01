# goblin-wg

**Wargaming API client and CLI toolkit for Python.**

Dynamically generates typed methods from the live WG API specification at runtime, with automatic type stub generation (`client.pyi`) so your editor knows about every endpoint without guessing.

Exposes multiple interfaces for the WG developer API as seen here: [Official WarGaming API Reference](https://developers.wargaming.net/reference/)

[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Features

- **Dynamic API methods** — all 28+ WoWS endpoints are bound automatically from the live `wows/` spec.
- **Auto-generated type stubs** — `client.pyi` is generated on first use and refreshed whenever the spec changes. Works with (based)Pyright, mypy, and Pylance out of the box.
- **Sensible cache defaults** — spec and stubs are stored in your platform's standard cache directory (`~/.cache/wg/wows`, `%LOCALAPPDATA%/wg/wows`, or `$XDG_CACHE_HOME/wg/wows`) or a custom location.
- **Minimal dependencies** — only `aiohttp` required at runtime.
- **PEP 561 compliant** — ships `py.typed`.

---

## Installation

**Plebians, knuckle-draggers** use:
```bash
pip install goblin-wg
```

**Sigmas**, with [uv](https://docs.astral.sh/uv/):
```bash
uv add goblin-wg
```

---

## Usage

### Python

```python
import asyncio
import wg.wows as wows


async def main():
    client = wows.WargamingAPIClient(application_id="YOUR_WG_APP_ID")

    # All API methods are dynamically bound with full IDE type hints
    players = await client.account_list(region="na", search="JesusLovesYouExceptSubs")
    info = await client.account_info(region="na", account_id=123456789)
    clan = await client.clans_info(region="na", clan_id=674206767, extra="members")


asyncio.run(main())
```

Custom storage path (e.g., within a project):

```python
client = wows.WargamingAPIClient(
    application_id="YOUR_WG_APP_ID",
    storage_path="/path/to/your/cache",
)
```

### AttrDict

All API responses are returned as `AttrDict` — a `dict` subclass with dot-access for convenience:

```python
players = await client.account_list(region="na", search="goblin")
for p in players:
    print(p.nickname, p.account_id)  # dot access works
```

---

## GDPR / Data Deletion Utility

Wargaming frequently requires developers to delete data for users who have requested account deletion, providing a `deleted_accounts.zip` file. `goblin-wg` includes built-in tools to make processing this trivial.

### Python API

```python
from wg.compliance import extract_deleted_account_ids

# Pass the path to the zip file (or raw accounts.csv) or its bytes
account_ids = extract_deleted_account_ids("deleted_accounts.zip")

for account_id in account_ids:
    # Example: Delete from your database
    db.execute("DELETE FROM players WHERE account_id = ?", (account_id,))
```

### CLI 

You can also use the CLI to easily pass these IDs into external scripts or pipelines:

```bash
# Outputs a JSON array of IDs
wg compliance extract-deleted deleted_accounts.zip

# Outputs a raw list of IDs, one per line
wg compliance extract-deleted deleted_accounts.zip --format text

# Pipe to another tool
wg compliance extract-deleted deleted_accounts.zip --format json | jq '.[]'
```

---

## CLI

The `wg` CLI is registered as a project script when installed:

```bash
# Show status of cached spec and stubs
wg wows info

# Generate or regenerate type stubs
wg wows generate-stubs
wg wows generate-stubs --force   # force even if stubs already exist

# Fetch the latest Wargaming API spec (and optionally regenerate stubs)
wg wows fetch-spec
wg wows fetch-spec --generate-stubs

# Shortcut: standalone stub generation (useful in CI or post-install hooks)
wg-stubgen --force
wg-stubgen --output /path/to/custom.pyi
```

### Auto-setup on first run

If you install `goblin-wg` into a new project and run `wg` without arguments, it will automatically detect missing stubs and run generation for you:

```sh
$ wg
Initial setup: WoWS type stubs not found. Autorunning type stub generation...
WoWS type stubs generated at: .../wg/wows/client.pyi
```

---

## Versioning

`goblin-wg` uses [Semantic Versioning](https://semver.org/).

The `wg.wows` submodule additionally tracks the WoWS game version it was
spec-built against:

```python
import wg
import wg.wows

print(wg.__version__)  # e.g. "1.0.0" — package version
print(wg.wows.__version__)  # e.g. "15.8.0" — WoWS game version at spec build time
```

---

## Regional Base URLs

All WoWS API endpoints use the pattern `{base_url}/wows/{method}/`.

| Region | Base URL | Code |
|--------|----------|------|
| North America | `https://api.worldofwarships.com` | `"na"` |
| Europe | `https://api.worldofwarships.eu` | `"eu"` |
| Asia | `https://api.worldofwarships.asia` | `"asia"` |
| Russia (👀) | `https://api.worldofwarships.ru` | `"ru"` |

Every request requires a `application_id`. Private endpoints additionally require an `access_token`.

---

## Development & Contributing

See [notes.md](notes.md) for architecture notes, endpoint coverage status, known gaps, and contribution guidelines.

---

## License

MIT — see [LICENSE](LICENSE) for details.
