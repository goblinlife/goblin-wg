# goblin-wg

**Wargaming API client and CLI toolkit for Python.**

Dynamically generates typed methods from the live WG API specification at runtime, with automatic type stub generation (`client.pyi`) so your editor knows about every endpoint without guessing.

Exposes multiple interfaces for the WG developer API as seen here: [Official WarGaming API Reference](https://developers.wargaming.net/reference/)

<p align="center">
  <a href="https://pypi.org/project/goblin-wg/"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/goblin-wg.svg?style=for-the-badge&logo=pypi&logoColor=white"></a>
  <a href="https://pypi.org/project/goblin-wg/"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/goblin-wg.svg?style=for-the-badge&color=blue"></a>
  <a href="https://python.org"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/goblin-wg.svg?style=for-the-badge&logo=python&logoColor=white"></a>
  <a href="https://github.com/goblinlife/goblin-wg/actions/workflows/publish.yml"><img alt="Build Status" src="https://img.shields.io/github/actions/workflow/status/goblinlife/goblin-wg/publish.yml?style=for-the-badge&logo=github"></a>
  <a href="https://github.com/goblinlife/goblin-wg/blob/main/LICENSE"><img alt="License: MIT" src="https://img.shields.io/github/license/goblinlife/goblin-wg.svg?style=for-the-badge"></a>
</p>

> [!NOTE]
> ### Attn 🐋🐳:
> This library is completely free and open-source. However, as a goblin, I am legally obligated to request tribute.
> If this package has helped stabilize your mental state or you just want to feed my insatiable greed, voluntary contributions are appreciated:
> <br>
> <a href="https://ko-fi.com/goblinlife"><img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Ko-fi" height="30"></a>&nbsp;
> <a href="https://github.com/sponsors/goblinlife"><img src="https://img.shields.io/badge/sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=#ea4aaa" alt="GitHub Sponsors" height="30"></a>

---

## Features

- **Dynamic API methods** — all 28+ WoWS and 62+ WoT endpoints are bound automatically from the live specs.
- **Auto-generated type stubs** — `client.pyi` is generated on first use and refreshed whenever the spec changes. Works with (based)Pyright, mypy, and Pylance out of the box.
- **Sensible cache defaults** — spec and stubs are stored in your platform's standard cache directory (`~/.cache/wg/<title>`, `%LOCALAPPDATA%/wg/<title>`, or `$XDG_CACHE_HOME/wg/<title>`) or a custom location.
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
import wg.wot as wot


async def main():
    wows_client = wows.WargamingAPIClient(application_id="YOUR_WG_APP_ID")
    wot_client = wot.WargamingAPIClient(application_id="YOUR_WG_APP_ID")

    # 1. Searching for an account (returns a list of AttrDicts)
    players = await wows_client.wows_account_list(region="na", search="JesusLovesYouExceptSubs")
    if not players:
        return

    account_id = players[0].account_id
    print(f"Found account ID: {account_id}")

    # 2. Fetching detailed stats (returns a dict keyed by the stringified ID)
    info_dict = await wows_client.wows_account_info(region="na", account_id=account_id)
    player_info = info_dict[str(account_id)]

    # 3. Accessing nested AttrDict data natively (using .pvp for Randoms stats)
    if hasattr(player_info.statistics, "pvp") and player_info.statistics.pvp:
        pvp_battles = player_info.statistics.pvp.get("battles", 0)
        pvp_wins = player_info.statistics.pvp.get("wins", 0)
        winrate = (pvp_wins / pvp_battles * 100) if pvp_battles > 0 else 0
        print(
            f"{player_info.nickname} has a {winrate:.2f}% PvP Winrate over {pvp_battles} battles!"
        )

    # WoT clients function identically with their respective dynamic methods
    tanks_players = await wot_client.wot_account_list(region="na", search="TankGamer1")


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
players = await wows_client.wows_account_list(region="na", search="goblin")
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
wg wot info

# Generate or regenerate type stubs
wg wows generate-stubs
wg wows generate-stubs --force   # force even if stubs already exist

# Fetch the latest Wargaming API spec (and optionally regenerate stubs)
wg wot fetch-spec
wg wot fetch-spec --generate-stubs
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

All API endpoints use the pattern `{base_url}/{title}/{method}/` (e.g. `wows` or `wot`).

| Region | WoWS Base URL | WoT Base URL | Code |
|--------|---------------|--------------|------|
| North America | `https://api.worldofwarships.com` | `https://api.worldoftanks.com` | `"na"` |
| Europe | `https://api.worldofwarships.eu` | `https://api.worldoftanks.eu` | `"eu"` |
| Asia | `https://api.worldofwarships.asia` | `https://api.worldoftanks.asia` | `"asia"` |
| Russia (👀) | `https://api.worldofwarships.ru` | `https://api.worldoftanks.ru` | `"ru"` |

Every request requires a `application_id`. Private endpoints additionally require an `access_token`.

---

## Development & Contributing

See [notes.md](notes.md) for architecture notes, endpoint coverage status, known gaps, and contribution guidelines.

---

## License

MIT — see [LICENSE](LICENSE) for details.
