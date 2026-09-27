# goblin-wg — Development Notes

1. This is not an official WarGaming repository. 
2. I am a goblin.

## Architecture

### How dynamic method binding works

On `WargamingAPIClient.__init__`, the client:

1. Probes `https://api.worldofwarships.com/wows/` with an `If-Modified-Since` header.
2. If the spec has changed (HTTP 200), saves the new JSON to the user's cache directory.
3. Loads the spec and iterates over `spec["methods"]`, binding each as an `async` method via `setattr`.
4. Calls `_stubgen.ensure_type_stubs()` — generating `client.pyi` if it doesn't exist.

The spec is a self-describing JSON document (~774 KB) returned by the root WG API URL. It contains every method name, URL, input/output fields, doc types, and enum values.

### Spec storage locations

| Platform | Default path |
|----------|-------------|
| Linux / other | `~/.cache/wg/wows/wows_api_spec.json` |
| macOS | `~/Library/Caches/wg/wows/wows_api_spec.json` |
| Windows | `%LOCALAPPDATA%/wg/wows/wows_api_spec.json` |
| XDG override | `$XDG_CACHE_HOME/wg/wows/wows_api_spec.json` |

A bundled fallback copy lives at `src/wg/wows/data/wows_api_spec.json` and is used when the network is unavailable and no cached copy exists.

---

## WoWS Official API — Complete Endpoint Inventory (28 methods as of 15.8.0)

### Account (3)

| Method key | Path | Required | Optional |
|------------|------|----------|----------|
| `account_list` | `/wows/account/list/` | `search` | `language`, `fields`, `type`, `limit` |
| `account_info` | `/wows/account/info/` | `account_id` | `language`, `fields`, `access_token`, `extra` |
| `account_achievements` | `/wows/account/achievements/` | `account_id` | `language`, `fields`, `access_token` |

> `extra` on `account_info` unlocks: `statistics.pvp_solo`, `pvp_div2`, `pvp_div3`, `rank_solo`, `rank_div2`, `rank_div3`, `club`, `pve`, `pve_solo`, `pve_div2`, `pve_div3`, `oper_solo`, `oper_div`, `oper_div_hard`, `statistics.clan`, `private.port`, `private.grouped_contacts`

### Clans (6)

| Method key | Path | Required | Notes |
|------------|------|----------|-------|
| `clans_list` | `/wows/clans/list/` | — | Min 2 chars for `search`. Returns `clan_id`, `tag`, `name`, `members_count`, `created_at` |
| `clans_info` | `/wows/clans/info/` | `clan_id` | `extra=members` returns full roster with `account_name`, `role`, `joined_at`. Also has `old_name`, `old_tag`, `renamed_at` (rename history) |
| `clans_accountinfo` | `/wows/clans/accountinfo/` | `account_id` | Player→Clan lookup, `joined_at`, `role`, `clan.tag`, `clan.name` |
| `clans_glossary` | `/wows/clans/glossary/` | — | Clan roles, settings, building definitions |
| `clans_season` | `/wows/clans/season/` | — | Season metadata: `season_id`, `ship_tier_min/max`, `start_time`, `finish_time` |
| `clans_seasonstats` | `/wows/clans/seasonstats/` | `account_id` | Per-player CB stats by season. Takes `account_id`, not `clan_id` |

### Encyclopedia (13)

| Method key | Path | Notes |
|------------|------|-------|
| `encyclopedia_info` | `/wows/encyclopedia/info/` | Game version, ship types, nations. Use for cache invalidation |
| `encyclopedia_ships` | `/wows/encyclopedia/ships/` | Paginated. 238 output fields incl. `default_profile`, `modules_tree`, `upgrades` |
| `encyclopedia_shipprofile` | `/wows/encyclopedia/shipprofile/` | Per-module-config computed stats |
| `encyclopedia_modules` | `/wows/encyclopedia/modules/` | Hulls, engines, fire control, etc |
| `encyclopedia_consumables` | `/wows/encyclopedia/consumables/` | Camos, flags, upgrades (modernizations) |
| `encyclopedia_achievements` | `/wows/encyclopedia/achievements/` | Achievement metadata |
| `encyclopedia_accountlevels` | `/wows/encyclopedia/accountlevels/` | SR tier → XP thresholds |
| `encyclopedia_crews` | `/wows/encyclopedia/crews/` | Commander info |
| `encyclopedia_crewskills` | `/wows/encyclopedia/crewskills/` | Skill definitions |
| `encyclopedia_crewranks` | `/wows/encyclopedia/crewranks/` | Rank names per nation |
| `encyclopedia_battlearenas` | `/wows/encyclopedia/battlearenas/` | Map names and metadata |
| `encyclopedia_collections` | `/wows/encyclopedia/collections/` | Collection definitions |
| `encyclopedia_collectioncards` | `/wows/encyclopedia/collectioncards/` | Individual card data |

### Ships (2)

| Method key | Path | Required |
|------------|------|----------|
| `ships_stats` | `/wows/ships/stats/` | `account_id` |
| `ships_badges` | `/wows/ships/badges/` | — |

### Seasons (2)

| Method key | Path | Notes |
|------------|------|-------|
| `seasons_info` | `/wows/seasons/info/` | Ranked season metadata |
| `seasons_shipstats` | `/wows/seasons/shipstats/` | Per-ship ranked stats |

### Warships (2)

| Method key | Path |
|------------|------|
| `warships_list` | `/wows/warships/list/` |
| `warships_badges` | `/wows/warships/badges/` |
