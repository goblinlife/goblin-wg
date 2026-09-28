"""
---
game_version: 15.8.0
updated_at: 2026-09-28T05:08:29.096170
fetch_date: Mon, 28 Sep 2026 09:08:28 GMT
content_language: en
---
"""

# AUTO-GENERATED STUB FILE - DO NOT EDIT
import logging
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Union

class AttrDict(dict[str, Any]):
    def __init__(self, mapping: Optional[Dict[str, Any]] = ..., **kwargs: Any) -> None: ...
    def __getattr__(self, item: str) -> Any: ...
    def __setattr__(self, key: str, value: Any) -> None: ...

class WargamingAPIClient:
    application_id: str
    storage_path: Path
    base_urls: Dict[str, str]
    def __init__(
        self,
        application_id: str,
        storage_path: str | Path | None = None,
        logger: logging.Logger | None = None,
    ) -> None: ...
    def _get_base_url(self, region: str) -> str: ...
    async def _request(self, region: str, endpoint: str, params: Dict[str, Any]) -> Any: ...
    async def wows_account_list(
        self,
        region: str,
        search: str,
        language: Literal[
            "cs", "de", "en", "es", "fr", "it", "ja", "pl", "ru", "th", "zh-tw", "zh-cn"
        ] = ...,
        fields: Union[
            Literal["account_id", "nickname"], List[Literal["account_id", "nickname"]], str
        ] = ...,
        type: Literal["startswith", "exact"] = ...,
        limit: int = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns partial list of players. The list is filtered by initial characters of user name and sorted alphabetically.
        """
        ...

    async def wows_account_info(
        self,
        region: str,
        account_id: Union[int, List[int], str],
        language: Literal[
            "cs", "de", "en", "es", "fr", "it", "ja", "pl", "ru", "th", "zh-tw", "zh-cn"
        ] = ...,
        fields: Union[
            Literal[
                "account_id",
                "created_at",
                "updated_at",
                "logout_at",
                "nickname",
                "last_battle_time",
                "leveling_points",
                "leveling_tier",
                "private",
                "statistics",
                "hidden_profile",
                "karma",
                "stats_updated_at",
            ],
            List[
                Literal[
                    "account_id",
                    "created_at",
                    "updated_at",
                    "logout_at",
                    "nickname",
                    "last_battle_time",
                    "leveling_points",
                    "leveling_tier",
                    "private",
                    "statistics",
                    "hidden_profile",
                    "karma",
                    "stats_updated_at",
                ]
            ],
            str,
        ] = ...,
        access_token: str = ...,
        extra: Union[
            Literal[
                "private.grouped_contacts",
                "private.port",
                "statistics.clan",
                "statistics.club",
                "statistics.oper_div",
                "statistics.oper_div_hard",
                "statistics.oper_solo",
                "statistics.pve",
                "statistics.pve_div2",
                "statistics.pve_div3",
                "statistics.pve_solo",
                "statistics.pvp_div2",
                "statistics.pvp_div3",
                "statistics.pvp_solo",
                "statistics.rank_div2",
                "statistics.rank_div3",
                "statistics.rank_solo",
            ],
            List[
                Literal[
                    "private.grouped_contacts",
                    "private.port",
                    "statistics.clan",
                    "statistics.club",
                    "statistics.oper_div",
                    "statistics.oper_div_hard",
                    "statistics.oper_solo",
                    "statistics.pve",
                    "statistics.pve_div2",
                    "statistics.pve_div3",
                    "statistics.pve_solo",
                    "statistics.pvp_div2",
                    "statistics.pvp_div3",
                    "statistics.pvp_solo",
                    "statistics.rank_div2",
                    "statistics.rank_div3",
                    "statistics.rank_solo",
                ]
            ],
        ] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns player details. Players may hide their game profiles, use field hidden_profile for determination.
        """
        ...

    async def wows_account_achievements(
        self,
        region: str,
        account_id: Union[int, List[int], str],
        language: Literal[
            "cs", "de", "en", "es", "fr", "it", "ja", "pl", "ru", "th", "zh-tw", "zh-cn"
        ] = ...,
        fields: Union[
            Literal["battle", "progress"], List[Literal["battle", "progress"]], str
        ] = ...,
        access_token: str = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns information about players' achievements. Accounts with hidden game profiles are excluded from response. Hidden profiles are listed in the field meta.hidden.
        """
        ...

    async def wows_clans_list(
        self,
        region: str,
        language: Literal[
            "cs", "de", "en", "es", "fr", "it", "ja", "pl", "ru", "th", "zh-tw", "zh-cn"
        ] = ...,
        fields: Union[
            Literal["clan_id", "name", "tag", "created_at", "members_count"],
            List[Literal["clan_id", "name", "tag", "created_at", "members_count"]],
            str,
        ] = ...,
        search: str = ...,
        limit: int = ...,
        page_no: int = ...,
        **kwargs,
    ) -> Any:
        """
        Method searches through clans and sorts them in a specified order.
        """
        ...

    async def wows_clans_info(
        self,
        region: str,
        clan_id: Union[int, List[int], str],
        language: Literal[
            "cs", "de", "en", "es", "fr", "it", "ja", "pl", "ru", "th", "zh-tw", "zh-cn"
        ] = ...,
        fields: Union[
            Literal[
                "clan_id",
                "name",
                "tag",
                "created_at",
                "members_count",
                "old_name",
                "old_tag",
                "renamed_at",
                "description",
                "is_clan_disbanded",
                "updated_at",
                "creator_id",
                "creator_name",
                "leader_id",
                "leader_name",
                "members_ids",
                "members",
            ],
            List[
                Literal[
                    "clan_id",
                    "name",
                    "tag",
                    "created_at",
                    "members_count",
                    "old_name",
                    "old_tag",
                    "renamed_at",
                    "description",
                    "is_clan_disbanded",
                    "updated_at",
                    "creator_id",
                    "creator_name",
                    "leader_id",
                    "leader_name",
                    "members_ids",
                    "members",
                ]
            ],
            str,
        ] = ...,
        extra: Union[Literal["members"], List[Literal["members"]]] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns detailed clan information.
        """
        ...

    async def wows_clans_accountinfo(
        self,
        region: str,
        account_id: Union[int, List[int], str],
        language: Literal[
            "cs", "de", "en", "es", "fr", "it", "ja", "pl", "ru", "th", "zh-tw", "zh-cn"
        ] = ...,
        fields: Union[
            Literal["account_id", "account_name", "joined_at", "role", "clan_id", "clan"],
            List[Literal["account_id", "account_name", "joined_at", "role", "clan_id", "clan"]],
            str,
        ] = ...,
        extra: Union[Literal["clan"], List[Literal["clan"]]] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns player clan data. Player clan data exist only for accounts, that were participating in clan activities: sent join requests, were clan members etc.
        """
        ...

    async def wows_clans_glossary(
        self,
        region: str,
        language: Literal[
            "cs", "de", "en", "es", "fr", "it", "ja", "pl", "ru", "th", "zh-tw", "zh-cn"
        ] = ...,
        fields: Union[
            Literal["clans_roles", "settings", "building_types", "buildings"],
            List[Literal["clans_roles", "settings", "building_types", "buildings"]],
            str,
        ] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns information on clan entities.
        """
        ...

    async def wows_clans_season(
        self,
        region: str,
        fields: Union[
            Literal[
                "season_id",
                "start_time",
                "finish_time",
                "division_points",
                "ship_tier_max",
                "ship_tier_min",
                "name",
                "leagues",
            ],
            List[
                Literal[
                    "season_id",
                    "start_time",
                    "finish_time",
                    "division_points",
                    "ship_tier_max",
                    "ship_tier_min",
                    "name",
                    "leagues",
                ]
            ],
            str,
        ] = ...,
        language: Literal[
            "cs",
            "de",
            "en",
            "es",
            "fr",
            "it",
            "ja",
            "pl",
            "ru",
            "th",
            "zh-tw",
            "zh-cn",
            "tr",
            "pt-br",
            "es-mx",
        ] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns information about Clan Battles season.
        """
        ...

    async def wows_clans_seasonstats(
        self,
        region: str,
        account_id: int,
        language: Literal[
            "cs", "de", "en", "es", "fr", "it", "ja", "pl", "ru", "th", "zh-tw", "zh-cn"
        ] = ...,
        fields: Union[
            Literal["account_id", "seasons"], List[Literal["account_id", "seasons"]], str
        ] = ...,
        access_token: str = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns clan battles season player stats.
        """
        ...

    async def wows_encyclopedia_info(
        self,
        region: str,
        fields: Union[
            Literal[
                "ship_types",
                "ship_type_images",
                "ship_nations",
                "ship_modules",
                "ship_modifications",
                "ships_updated_at",
                "game_version",
                "languages",
            ],
            List[
                Literal[
                    "ship_types",
                    "ship_type_images",
                    "ship_nations",
                    "ship_modules",
                    "ship_modifications",
                    "ships_updated_at",
                    "game_version",
                    "languages",
                ]
            ],
            str,
        ] = ...,
        language: Literal[
            "cs",
            "de",
            "en",
            "es",
            "fr",
            "it",
            "ja",
            "pl",
            "ru",
            "th",
            "zh-tw",
            "zh-cn",
            "tr",
            "pt-br",
            "es-mx",
        ] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns information about encyclopedia.
        """
        ...

    async def wows_encyclopedia_ships(
        self,
        region: str,
        fields: Union[
            Literal[
                "ship_id",
                "ship_id_str",
                "name",
                "description",
                "nation",
                "next_ships",
                "type",
                "tier",
                "price_credit",
                "price_gold",
                "is_premium",
                "has_demo_profile",
                "mod_slots",
                "default_profile",
                "modules",
                "modules_tree",
                "upgrades",
                "images",
                "is_special",
            ],
            List[
                Literal[
                    "ship_id",
                    "ship_id_str",
                    "name",
                    "description",
                    "nation",
                    "next_ships",
                    "type",
                    "tier",
                    "price_credit",
                    "price_gold",
                    "is_premium",
                    "has_demo_profile",
                    "mod_slots",
                    "default_profile",
                    "modules",
                    "modules_tree",
                    "upgrades",
                    "images",
                    "is_special",
                ]
            ],
            str,
        ] = ...,
        language: Literal[
            "cs",
            "de",
            "en",
            "es",
            "fr",
            "it",
            "ja",
            "pl",
            "ru",
            "th",
            "zh-tw",
            "zh-cn",
            "tr",
            "pt-br",
            "es-mx",
        ] = ...,
        page_no: int = ...,
        limit: int = ...,
        ship_id: Union[int, List[int], str] = ...,
        nation: Union[str, List[str]] = ...,
        type: Union[
            Literal["AirCarrier", "Battleship", "Destroyer", "Cruiser", "Submarine"],
            List[Literal["AirCarrier", "Battleship", "Destroyer", "Cruiser", "Submarine"]],
        ] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns list of ships available.
        """
        ...

    async def wows_encyclopedia_achievements(
        self,
        region: str,
        fields: Union[Literal["battle"], List[Literal["battle"]], str] = ...,
        language: Literal[
            "cs",
            "de",
            "en",
            "es",
            "fr",
            "it",
            "ja",
            "pl",
            "ru",
            "th",
            "zh-tw",
            "zh-cn",
            "tr",
            "pt-br",
            "es-mx",
        ] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns information about achievements.
        """
        ...

    async def wows_encyclopedia_shipprofile(
        self,
        region: str,
        ship_id: int,
        fields: Union[
            Literal[
                "battle_level_range_min",
                "battle_level_range_max",
                "hull",
                "engine",
                "artillery",
                "torpedoes",
                "fire_control",
                "flight_control",
                "fighters",
                "torpedo_bomber",
                "dive_bomber",
                "submarine_sonar",
                "atbas",
                "anti_aircraft",
                "armour",
                "mobility",
                "concealment",
                "weaponry",
                "submarine_mobility",
                "submarine_battery",
                "depth_charge",
                "ship_id",
            ],
            List[
                Literal[
                    "battle_level_range_min",
                    "battle_level_range_max",
                    "hull",
                    "engine",
                    "artillery",
                    "torpedoes",
                    "fire_control",
                    "flight_control",
                    "fighters",
                    "torpedo_bomber",
                    "dive_bomber",
                    "submarine_sonar",
                    "atbas",
                    "anti_aircraft",
                    "armour",
                    "mobility",
                    "concealment",
                    "weaponry",
                    "submarine_mobility",
                    "submarine_battery",
                    "depth_charge",
                    "ship_id",
                ]
            ],
            str,
        ] = ...,
        language: Literal[
            "cs",
            "de",
            "en",
            "es",
            "fr",
            "it",
            "ja",
            "pl",
            "ru",
            "th",
            "zh-tw",
            "zh-cn",
            "tr",
            "pt-br",
            "es-mx",
        ] = ...,
        artillery_id: int = ...,
        torpedoes_id: int = ...,
        fire_control_id: int = ...,
        flight_control_id: int = ...,
        hull_id: int = ...,
        engine_id: int = ...,
        fighter_id: int = ...,
        dive_bomber_id: int = ...,
        torpedo_bomber_id: int = ...,
        submarine_sonar_id: int = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns parameters of ships in all existing configurations.
        """
        ...

    async def wows_encyclopedia_modules(
        self,
        region: str,
        fields: Union[
            Literal[
                "module_id",
                "module_id_str",
                "tag",
                "name",
                "type",
                "image",
                "price_credit",
                "profile",
            ],
            List[
                Literal[
                    "module_id",
                    "module_id_str",
                    "tag",
                    "name",
                    "type",
                    "image",
                    "price_credit",
                    "profile",
                ]
            ],
            str,
        ] = ...,
        language: Literal[
            "cs",
            "de",
            "en",
            "es",
            "fr",
            "it",
            "ja",
            "pl",
            "ru",
            "th",
            "zh-tw",
            "zh-cn",
            "tr",
            "pt-br",
            "es-mx",
        ] = ...,
        page_no: int = ...,
        limit: int = ...,
        module_id: Union[int, List[int], str] = ...,
        type: Literal[
            "Artillery",
            "Torpedoes",
            "Suo",
            "FlightControl",
            "Hull",
            "Engine",
            "Fighter",
            "TorpedoBomber",
            "DiveBomber",
            "Sonar",
        ] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns list of available modules that can be mounted on a ship (hull, engines, etc.).
        """
        ...

    async def wows_encyclopedia_consumables(
        self,
        region: str,
        fields: Union[
            Literal[
                "consumable_id",
                "type",
                "name",
                "description",
                "price_credit",
                "price_gold",
                "image",
                "profile",
            ],
            List[
                Literal[
                    "consumable_id",
                    "type",
                    "name",
                    "description",
                    "price_credit",
                    "price_gold",
                    "image",
                    "profile",
                ]
            ],
            str,
        ] = ...,
        language: Literal[
            "cs",
            "de",
            "en",
            "es",
            "fr",
            "it",
            "ja",
            "pl",
            "ru",
            "th",
            "zh-tw",
            "zh-cn",
            "tr",
            "pt-br",
            "es-mx",
        ] = ...,
        limit: int = ...,
        consumable_id: Union[int, List[int], str] = ...,
        type: Literal["Camouflage", "Flags", "Permoflage", "Modernization", "Skin"] = ...,
        page_no: int = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns information about consumables: camouflages, flags, and upgrades.
        """
        ...

    async def wows_encyclopedia_accountlevels(
        self,
        region: str,
        fields: Union[
            Literal["tier", "points", "image"], List[Literal["tier", "points", "image"]], str
        ] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns information about Service Record levels.
        """
        ...

    async def wows_encyclopedia_crews(
        self,
        region: str,
        fields: Union[
            Literal[
                "base_training_level",
                "gold_training_hire_price",
                "gold_retraining_price",
                "money_training_hire_price",
                "nation",
                "base_training_hire_price",
                "money_retraining_price",
                "money_training_level",
                "is_retrainable",
                "gold_training_level",
                "icons",
                "first_names",
                "last_names",
                "subnation_index",
            ],
            List[
                Literal[
                    "base_training_level",
                    "gold_training_hire_price",
                    "gold_retraining_price",
                    "money_training_hire_price",
                    "nation",
                    "base_training_hire_price",
                    "money_retraining_price",
                    "money_training_level",
                    "is_retrainable",
                    "gold_training_level",
                    "icons",
                    "first_names",
                    "last_names",
                    "subnation_index",
                ]
            ],
            str,
        ] = ...,
        language: Literal[
            "cs",
            "de",
            "en",
            "es",
            "fr",
            "it",
            "ja",
            "pl",
            "ru",
            "th",
            "zh-tw",
            "zh-cn",
            "tr",
            "pt-br",
            "es-mx",
        ] = ...,
        commander_id: Union[int, List[int], str] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns information about Commanders.
        """
        ...

    async def wows_encyclopedia_crewskills(
        self,
        region: str,
        fields: Union[
            Literal["name", "icon", "type_id", "type_name", "customization"],
            List[Literal["name", "icon", "type_id", "type_name", "customization"]],
            str,
        ] = ...,
        language: Literal[
            "cs",
            "de",
            "en",
            "es",
            "fr",
            "it",
            "ja",
            "pl",
            "ru",
            "th",
            "zh-tw",
            "zh-cn",
            "tr",
            "pt-br",
            "es-mx",
        ] = ...,
        skill_id: Union[int, List[int], str] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns information about Commanders' skills.
        """
        ...

    async def wows_encyclopedia_crewranks(
        self,
        region: str,
        fields: Union[
            Literal["rank", "name", "names", "experience"],
            List[Literal["rank", "name", "names", "experience"]],
            str,
        ] = ...,
        language: Literal[
            "cs",
            "de",
            "en",
            "es",
            "fr",
            "it",
            "ja",
            "pl",
            "ru",
            "th",
            "zh-tw",
            "zh-cn",
            "tr",
            "pt-br",
            "es-mx",
        ] = ...,
        nation: str = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns information about Commanders' ranks.
        """
        ...

    async def wows_encyclopedia_battletypes(
        self,
        region: str,
        fields: Union[
            Literal["name", "tag", "description", "image"],
            List[Literal["name", "tag", "description", "image"]],
            str,
        ] = ...,
        language: Literal[
            "cs",
            "de",
            "en",
            "es",
            "fr",
            "it",
            "ja",
            "pl",
            "ru",
            "th",
            "zh-tw",
            "zh-cn",
            "tr",
            "pt-br",
            "es-mx",
        ] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns information about battle types.
        """
        ...

    async def wows_encyclopedia_collections(
        self,
        region: str,
        fields: Union[
            Literal["collection_id", "name", "tag", "description", "image", "card_cost"],
            List[Literal["collection_id", "name", "tag", "description", "image", "card_cost"]],
            str,
        ] = ...,
        language: Literal[
            "cs",
            "de",
            "en",
            "es",
            "fr",
            "it",
            "ja",
            "pl",
            "ru",
            "th",
            "zh-tw",
            "zh-cn",
            "tr",
            "pt-br",
            "es-mx",
        ] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns information about collections.
        """
        ...

    async def wows_encyclopedia_collectioncards(
        self,
        region: str,
        fields: Union[
            Literal["card_id", "collection_id", "name", "tag", "description", "images"],
            List[Literal["card_id", "collection_id", "name", "tag", "description", "images"]],
            str,
        ] = ...,
        language: Literal[
            "cs",
            "de",
            "en",
            "es",
            "fr",
            "it",
            "ja",
            "pl",
            "ru",
            "th",
            "zh-tw",
            "zh-cn",
            "tr",
            "pt-br",
            "es-mx",
        ] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns information about items that are included in the collection.
        """
        ...

    async def wows_encyclopedia_battlearenas(
        self,
        region: str,
        fields: Union[
            Literal["battle_arena_id", "name", "description", "icon"],
            List[Literal["battle_arena_id", "name", "description", "icon"]],
            str,
        ] = ...,
        language: Literal[
            "cs",
            "de",
            "en",
            "es",
            "fr",
            "it",
            "ja",
            "pl",
            "ru",
            "th",
            "zh-tw",
            "zh-cn",
            "tr",
            "pt-br",
            "es-mx",
        ] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns the information about maps.
        """
        ...

    async def wows_ships_stats(
        self,
        region: str,
        account_id: int,
        language: Literal[
            "cs", "de", "en", "es", "fr", "it", "ja", "pl", "ru", "th", "zh-tw", "zh-cn"
        ] = ...,
        fields: Union[
            Literal[
                "battles",
                "distance",
                "pvp",
                "pve",
                "pvp_solo",
                "pve_solo",
                "pvp_div2",
                "pve_div2",
                "pvp_div3",
                "pve_div3",
                "rank_solo",
                "rank_div2",
                "rank_div3",
                "club",
                "clan",
                "oper_solo",
                "oper_div",
                "oper_div_hard",
                "account_id",
                "ship_id",
                "last_battle_time",
                "updated_at",
                "private",
            ],
            List[
                Literal[
                    "battles",
                    "distance",
                    "pvp",
                    "pve",
                    "pvp_solo",
                    "pve_solo",
                    "pvp_div2",
                    "pve_div2",
                    "pvp_div3",
                    "pve_div3",
                    "rank_solo",
                    "rank_div2",
                    "rank_div3",
                    "club",
                    "clan",
                    "oper_solo",
                    "oper_div",
                    "oper_div_hard",
                    "account_id",
                    "ship_id",
                    "last_battle_time",
                    "updated_at",
                    "private",
                ]
            ],
            str,
        ] = ...,
        access_token: str = ...,
        extra: Union[
            Literal[
                "clan",
                "club",
                "oper_div",
                "oper_div_hard",
                "oper_solo",
                "pve",
                "pve_div2",
                "pve_div3",
                "pve_solo",
                "pvp_div2",
                "pvp_div3",
                "pvp_solo",
                "rank_div2",
                "rank_div3",
                "rank_solo",
            ],
            List[
                Literal[
                    "clan",
                    "club",
                    "oper_div",
                    "oper_div_hard",
                    "oper_solo",
                    "pve",
                    "pve_div2",
                    "pve_div3",
                    "pve_solo",
                    "pvp_div2",
                    "pvp_div3",
                    "pvp_solo",
                    "rank_div2",
                    "rank_div3",
                    "rank_solo",
                ]
            ],
        ] = ...,
        ship_id: Union[int, List[int], str] = ...,
        in_garage: Literal["1", "0"] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns general statistics for each ship of a player. Accounts with hidden game profiles are excluded from response. Hidden profiles are listed in the field meta.hidden.
        """
        ...

    async def wows_ships_badges(
        self,
        region: str,
        account_id: int,
        language: Literal[
            "cs", "de", "en", "es", "fr", "it", "ja", "pl", "ru", "th", "zh-tw", "zh-cn"
        ] = ...,
        fields: Union[
            Literal["ship_id", "top_grade_class"], List[Literal["ship_id", "top_grade_class"]], str
        ] = ...,
        ship_id: Union[int, List[int], str] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns badges for player's ships.
        """
        ...

    async def wows_seasons_info(
        self,
        region: str,
        fields: Union[
            Literal[
                "season_id",
                "season_name",
                "account_tier",
                "start_at",
                "finish_at",
                "close_at",
                "leagues",
            ],
            List[
                Literal[
                    "season_id",
                    "season_name",
                    "account_tier",
                    "start_at",
                    "finish_at",
                    "close_at",
                    "leagues",
                ]
            ],
            str,
        ] = ...,
        language: Literal[
            "cs",
            "de",
            "en",
            "es",
            "fr",
            "it",
            "ja",
            "pl",
            "ru",
            "th",
            "zh-tw",
            "zh-cn",
            "tr",
            "pt-br",
            "es-mx",
        ] = ...,
        season_id: Union[int, List[int], str] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns information about Ranked Battles seasons.
        """
        ...

    async def wows_seasons_shipstats(
        self,
        region: str,
        account_id: int,
        language: Literal[
            "cs", "de", "en", "es", "fr", "it", "ja", "pl", "ru", "th", "zh-tw", "zh-cn"
        ] = ...,
        fields: Union[
            Literal["account_id", "ship_id", "seasons"],
            List[Literal["account_id", "ship_id", "seasons"]],
            str,
        ] = ...,
        access_token: str = ...,
        season_id: Union[int, List[int], str] = ...,
        ship_id: Union[int, List[int], str] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns players' ships statistics in Ranked Battles seasons. Accounts with hidden game profiles are excluded from response. Hidden profiles are listed in the field meta.hidden.
        """
        ...

    async def wows_seasons_accountinfo(
        self,
        region: str,
        account_id: Union[int, List[int], str],
        language: Literal[
            "cs", "de", "en", "es", "fr", "it", "ja", "pl", "ru", "th", "zh-tw", "zh-cn"
        ] = ...,
        fields: Union[
            Literal["account_id", "seasons", "rank_info"],
            List[Literal["account_id", "seasons", "rank_info"]],
            str,
        ] = ...,
        access_token: str = ...,
        season_id: Union[int, List[int], str] = ...,
        **kwargs,
    ) -> Any:
        """
        Method returns players' statistics in Ranked Battles seasons. Accounts with hidden game profiles are excluded from response. Hidden profiles are listed in the field meta.hidden.
        """
        ...
