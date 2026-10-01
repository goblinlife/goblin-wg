# goblin-wg — Development Notes

1. This is not an official WarGaming repository. 
2. I am a goblin.

## Architecture

### How dynamic method binding works

On `WargamingAPIClient.__init__`, the client:

1. Probes `https://api.worldofwarships.com/wows/` (or the equivalent tanks URL) with an `If-Modified-Since` header.
2. If the spec has changed (HTTP 200), saves the new JSON to the user's cache directory.
3. Loads the spec and iterates over `spec["methods"]`, binding each as an `async` method via `setattr`.
4. Calls `_stubgen.ensure_type_stubs()` — generating `client.pyi` if it doesn't exist.

The spec is a self-describing JSON document (~774 KB) returned by the root WG API URL. It contains every method name, URL, input/output fields, doc types, and enum values.

### Spec storage locations

| Platform | Default path |
|----------|-------------|
| Linux / other | `~/.cache/wg/<title>/<title>_api_spec.json` |
| macOS | `~/Library/Caches/wg/<title>/<title>_api_spec.json` |
| Windows | `%LOCALAPPDATA%/wg/<title>/<title>_api_spec.json` |
| XDG override | `$XDG_CACHE_HOME/wg/<title>/<title>_api_spec.json` |

A bundled fallback copy lives at `src/wg/<title>/data/<title>_api_spec.json` and is used when the network is unavailable and no cached copy exists.

---

## Usage Gotchas & Tips

When working with the responses from the API, keep these nuances in mind:

1. **Stringified IDs in Responses:** Endpoints that fetch info for specific IDs (e.g. `account_info`, `clans_info`, `ships_stats`) return dictionaries where the keys are the **stringified IDs**.
   ```python
   # DO THIS:
   response = await client.wows_account_info(region="na", account_id=12345)
   player = response["12345"] 
   ```
2. **Lists vs Dictionaries:** Search endpoints (e.g., `wows_account_list`, `wows_clans_list`) typically return flat `list`s of objects. Info endpoints return nested `dict`s.
3. **PvP Stats vs Global Stats:** When pulling account statistics (`player.statistics`), the top-level `.battles` represents ALL lifetime battles including Co-Op. To calculate Random Battle winrates, you must pull from the nested `pvp` structure:
   ```python
   pvp_battles = player.statistics.pvp.battles
   pvp_wins = player.statistics.pvp.wins
   ```

---

## WoWS Official API — Complete Endpoint Inventory (28 methods as of 15.8.0)

### Account (3)

| Method key | Path | Required | Optional |
|------------|------|----------|----------|
| `wows_account_list` | `/wows/account/list/` | `search` | `language`, `fields`, `type`, `limit` |
| `wows_account_info` | `/wows/account/info/` | `account_id` | `language`, `fields`, `access_token`, `extra` |
| `wows_account_achievements` | `/wows/account/achievements/` | `account_id` | `language`, `fields`, `access_token` |

> `extra` on `account_info` unlocks: `statistics.pvp_solo`, `pvp_div2`, `pvp_div3`, `rank_solo`, `rank_div2`, `rank_div3`, `club`, `pve`, `pve_solo`, `pve_div2`, `pve_div3`, `oper_solo`, `oper_div`, `oper_div_hard`, `statistics.clan`, `private.port`, `private.grouped_contacts`

### Clans (6)

| Method key | Path | Required | Notes |
|------------|------|----------|-------|
| `wows_clans_list` | `/wows/clans/list/` | — | Min 2 chars for `search`. Returns `clan_id`, `tag`, `name`, `members_count`, `created_at` |
| `wows_clans_info` | `/wows/clans/info/` | `clan_id` | `extra=members` returns full roster with `account_name`, `role`, `joined_at`. Also has `old_name`, `old_tag`, `renamed_at` (rename history) |
| `wows_clans_accountinfo` | `/wows/clans/accountinfo/` | `account_id` | Player→Clan lookup, `joined_at`, `role`, `clan.tag`, `clan.name` |
| `wows_clans_glossary` | `/wows/clans/glossary/` | — | Clan roles, settings, building definitions |
| `wows_clans_season` | `/wows/clans/season/` | — | Season metadata: `season_id`, `ship_tier_min/max`, `start_time`, `finish_time` |
| `wows_clans_seasonstats` | `/wows/clans/seasonstats/` | `account_id` | Per-player CB stats by season. Takes `account_id`, not `clan_id` |

### Encyclopedia (13)

| Method key | Path | Notes |
|------------|------|-------|
| `wows_encyclopedia_info` | `/wows/encyclopedia/info/` | Game version, ship types, nations. Use for cache invalidation |
| `wows_encyclopedia_ships` | `/wows/encyclopedia/ships/` | Paginated. 238 output fields incl. `default_profile`, `modules_tree`, `upgrades` |
| `wows_encyclopedia_shipprofile` | `/wows/encyclopedia/shipprofile/` | Per-module-config computed stats |
| `wows_encyclopedia_modules` | `/wows/encyclopedia/modules/` | Hulls, engines, fire control, etc |
| `wows_encyclopedia_consumables` | `/wows/encyclopedia/consumables/` | Camos, flags, upgrades (modernizations) |
| `wows_encyclopedia_achievements` | `/wows/encyclopedia/achievements/` | Achievement metadata |
| `wows_encyclopedia_accountlevels` | `/wows/encyclopedia/accountlevels/` | SR tier → XP thresholds |
| `wows_encyclopedia_crews` | `/wows/encyclopedia/crews/` | Commander info |
| `wows_encyclopedia_crewskills` | `/wows/encyclopedia/crewskills/` | Skill definitions |
| `wows_encyclopedia_crewranks` | `/wows/encyclopedia/crewranks/` | Rank names per nation |
| `wows_encyclopedia_battlearenas` | `/wows/encyclopedia/battlearenas/` | Map names and metadata |
| `wows_encyclopedia_collections` | `/wows/encyclopedia/collections/` | Collection definitions |
| `wows_encyclopedia_collectioncards` | `/wows/encyclopedia/collectioncards/` | Individual card data |

### Ships (2)

| Method key | Path | Required |
|------------|------|----------|
| `wows_ships_stats` | `/wows/ships/stats/` | `account_id` |
| `wows_ships_badges` | `/wows/ships/badges/` | — |

### Seasons (2)

| Method key | Path | Notes |
|------------|------|-------|
| `wows_seasons_info` | `/wows/seasons/info/` | Ranked season metadata |
| `wows_seasons_shipstats` | `/wows/seasons/shipstats/` | Per-ship ranked stats |

### Warships (2)

| Method key | Path |
|------------|------|
| `wows_warships_list` | `/wows/warships/list/` |
| `wows_warships_badges` | `/wows/warships/badges/` |
