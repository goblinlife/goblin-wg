"""
---
game_version: 2.4
updated_at: 2026-10-01T01:07:54.621102
fetch_date: Thu, 01 Oct 2026 05:07:54 GMT
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
    def __init__(self, application_id: str, storage_path: str | Path | None = None, logger: logging.Logger | None = None) -> None: ...
    def _get_base_url(self, region: str) -> str: ...
    async def _request(self, region: str, endpoint: str, params: Dict[str, Any]) -> Any: ...

    async def wot_account_list(self, region: str, search: str, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['account_id', 'nickname'], List[Literal['account_id', 'nickname']], str] = ..., type: Literal['startswith', 'exact'] = ..., limit: int = ..., **kwargs) -> Any:
        """
        Method returns partial list of players. The list is filtered by initial characters of user name and sorted alphabetically.
        """
        ...

    async def wot_account_info(self, region: str, account_id: Union[int, List[int], str], language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['statistics', 'account_id', 'created_at', 'updated_at', 'logout_at', 'last_battle_time', 'nickname', 'global_rating', 'private', 'client_language', 'clan_id'], List[Literal['statistics', 'account_id', 'created_at', 'updated_at', 'logout_at', 'last_battle_time', 'nickname', 'global_rating', 'private', 'client_language', 'clan_id']], str] = ..., access_token: str = ..., extra: Union[Literal['private.boosters', 'private.garage', 'private.grouped_contacts', 'private.personal_missions', 'private.rented', 'statistics.epic', 'statistics.fallout', 'statistics.globalmap_absolute', 'statistics.globalmap_champion', 'statistics.globalmap_middle', 'statistics.random', 'statistics.ranked_10x10', 'statistics.ranked_15x15', 'statistics.ranked_battles', 'statistics.ranked_battles_current', 'statistics.ranked_battles_previous', 'statistics.ranked_season_1', 'statistics.ranked_season_2', 'statistics.ranked_season_3'], List[Literal['private.boosters', 'private.garage', 'private.grouped_contacts', 'private.personal_missions', 'private.rented', 'statistics.epic', 'statistics.fallout', 'statistics.globalmap_absolute', 'statistics.globalmap_champion', 'statistics.globalmap_middle', 'statistics.random', 'statistics.ranked_10x10', 'statistics.ranked_15x15', 'statistics.ranked_battles', 'statistics.ranked_battles_current', 'statistics.ranked_battles_previous', 'statistics.ranked_season_1', 'statistics.ranked_season_2', 'statistics.ranked_season_3']]] = ..., **kwargs) -> Any:
        """
        Method returns player details.
        """
        ...

    async def wot_account_tanks(self, region: str, account_id: Union[int, List[int], str], language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['tank_id', 'mark_of_mastery', 'statistics'], List[Literal['tank_id', 'mark_of_mastery', 'statistics']], str] = ..., access_token: str = ..., tank_id: Union[int, List[int], str] = ..., **kwargs) -> Any:
        """
        Method returns details on player's vehicles.
        """
        ...

    async def wot_account_achievements(self, region: str, account_id: Union[int, List[int], str], language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['achievements', 'max_series', 'frags'], List[Literal['achievements', 'max_series', 'frags']], str] = ..., **kwargs) -> Any:
        """
        Method returns players' achievement details.
        
        Achievement properties define the **achievements** field values:
        
         * 1-4 for Mastery Badges and Stage Achievements (type: "class");
         * maximum value of Achievement series (type: "series");
         * number of achievements earned from sections: Battle Hero, Epic Achievements, Group Achievements, Special Achievements, etc. (type: "repeatable, single, custom").
        
        """
        ...

    async def wot_account_wtr(self, region: str, account_id: Union[int, List[int], str], language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['account_id', 'rating'], List[Literal['account_id', 'rating']], str] = ..., **kwargs) -> Any:
        """
        Method returns player WTR rating
        """
        ...

    async def wot_auth_login(self, region: str, expires_at: int = ..., redirect_uri: str = ..., display: Literal['page', 'popup'] = ..., nofollow: int = ..., **kwargs) -> Any:
        """
        Method authenticates user based on Wargaming.net ID (OpenID) which is used in World of Tanks, World of Tanks Blitz, World of Warships, World of Warplanes, and WarGag.ru. To log in, player must enter email and password used for creating account, or use a social network profile.
        Authentication is not available for iOS Game Center users in the following cases:
        *  the account is not linked to a social network account, or
        *  email and password are not specified in the profile.
        
        Information on authorization status is sent to URL specified in **redirect_uri** parameter.
        
        If authentication is successful, the following parameters are sent to **redirect_uri**:
        
        *  **status: ok** — successful authentication
        *  **access_token** — access token is passed in to all methods that require authentication
        *  **expires_at** — expiration date of **access_token**
        *  **account_id** — user ID
        *  **nickname** — user name.
        
        If authentication fails, the following parameters are sent to **redirect_uri**:
        
        *  **status: error** — authentication error
        *  **code** — error code
        *  **message** — error message.
        """
        ...

    async def wot_auth_prolongate(self, region: str, access_token: str, expires_at: int = ..., **kwargs) -> Any:
        """
        Method generates new **access_token** based on the current token.
        
        This method is used when the player is still using the application but the current **access_token** is about to expire.
        """
        ...

    async def wot_auth_logout(self, region: str, access_token: str, **kwargs) -> Any:
        """
        Method deletes user's **access_token**.
        
        After this method is called, **access_token** becomes invalid.
        """
        ...

    async def wot_clans_list(self, region: str, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['clan_id', 'name', 'tag', 'created_at', 'color', 'members_count', 'emblems'], List[Literal['clan_id', 'name', 'tag', 'created_at', 'color', 'members_count', 'emblems']], str] = ..., search: str = ..., limit: int = ..., page_no: int = ..., **kwargs) -> Any:
        """
        Method searches through clans and sorts them in a specified order.
        """
        ...

    async def wot_clans_info(self, region: str, clan_id: Union[int, List[int], str], language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['clan_id', 'name', 'tag', 'created_at', 'color', 'members_count', 'emblems', 'old_name', 'old_tag', 'renamed_at', 'description', 'description_html', 'motto', 'is_clan_disbanded', 'accepts_join_requests', 'updated_at', 'creator_id', 'creator_name', 'leader_id', 'leader_name', 'members', 'private'], List[Literal['clan_id', 'name', 'tag', 'created_at', 'color', 'members_count', 'emblems', 'old_name', 'old_tag', 'renamed_at', 'description', 'description_html', 'motto', 'is_clan_disbanded', 'accepts_join_requests', 'updated_at', 'creator_id', 'creator_name', 'leader_id', 'leader_name', 'members', 'private']], str] = ..., access_token: str = ..., extra: Union[Literal['private.online_members'], List[Literal['private.online_members']]] = ..., members_key: Literal['id'] = ..., **kwargs) -> Any:
        """
        Method returns detailed clan information.
        """
        ...

    async def wot_clans_accountinfo(self, region: str, account_id: Union[int, List[int], str], language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['account_id', 'account_name', 'joined_at', 'role', 'role_i18n', 'clan'], List[Literal['account_id', 'account_name', 'joined_at', 'role', 'role_i18n', 'clan']], str] = ..., **kwargs) -> Any:
        """
        Method returns detailed clan member information and brief clan details.
        """
        ...

    async def wot_clans_glossary(self, region: str, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['clans_roles'], List[Literal['clans_roles']], str] = ..., **kwargs) -> Any:
        """
        Method returns information on clan entities.
        """
        ...

    async def wot_clans_messageboard(self, region: str, access_token: str, fields: Union[Literal['message', 'created_at', 'updated_at', 'author_id', 'editor_id', 'is_read'], List[Literal['message', 'created_at', 'updated_at', 'author_id', 'editor_id', 'is_read']], str] = ..., **kwargs) -> Any:
        """
        Method returns messages of clan message board.<p/>This method will be removed. Use method <a href="/reference/all/wot/clans/messageboard/">Message board (World of Tanks)</a>
        """
        ...

    async def wot_clans_memberhistory(self, region: str, account_id: int, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['account_id', 'clan_id', 'joined_at', 'left_at', 'role'], List[Literal['account_id', 'clan_id', 'joined_at', 'left_at', 'role']], str] = ..., **kwargs) -> Any:
        """
        Method returns information about player's clan history. Data on 10 last clan memberships are presented in the response.<p/>This method will be removed. Use method <a href="/reference/all/wot/clans/memberhistory/">Player's clan history (World of Tanks)</a>
        """
        ...

    async def wot_stronghold_claninfo(self, region: str, clan_id: Union[int, List[int], str], fields: Union[Literal['clan_id', 'clan_name', 'clan_tag', 'stronghold_level', 'stronghold_buildings_level', 'command_center_arena_id', 'building_slots', 'skirmish_statistics', 'battles_for_strongholds_statistics', 'battles_series_for_strongholds_statistics'], List[Literal['clan_id', 'clan_name', 'clan_tag', 'stronghold_level', 'stronghold_buildings_level', 'command_center_arena_id', 'building_slots', 'skirmish_statistics', 'battles_for_strongholds_statistics', 'battles_series_for_strongholds_statistics']], str] = ..., language: Literal['en', 'fr', 'es-ar', 'pt-br', 'ja'] = ..., **kwargs) -> Any:
        """
        Method returns general information and the battle statistics of clans in the Stronghold mode. Please note that information about the number of battles fought as well as the number of defeats and victories is updated once every 24 hours.
        """
        ...

    async def wot_stronghold_clanreserves(self, region: str, access_token: str, fields: Union[Literal['name', 'type', 'disposable', 'bonus_type', 'icon', 'in_stock'], List[Literal['name', 'type', 'disposable', 'bonus_type', 'icon', 'in_stock']], str] = ..., language: Literal['en', 'fr', 'es-ar', 'pt-br', 'ja'] = ..., **kwargs) -> Any:
        """
        Method returns information about available Reserves and their current status.
        """
        ...

    async def wot_stronghold_activateclanreserve(self, region: str, access_token: str, reserve_type: str, reserve_level: int, fields: Union[Literal['activated_at'], List[Literal['activated_at']], str] = ..., language: Literal['en', 'fr', 'es-ar', 'pt-br', 'ja'] = ..., **kwargs) -> Any:
        """
        This method activates an available clan Reserve. A clan Reserve can be activated only by a clan member with the required permission.
        """
        ...

    async def wot_globalmap_fronts(self, region: str, fields: Union[Literal['front_id', 'front_name', 'is_active', 'is_event', 'vehicle_freeze', 'fog_of_war', 'battle_time_limit', 'min_tanks_per_division', 'max_tanks_per_division', 'division_cost', 'avg_clans_rating', 'avg_won_bet', 'avg_min_bet', 'min_vehicle_level', 'max_vehicle_level', 'available_extensions', 'provinces_count'], List[Literal['front_id', 'front_name', 'is_active', 'is_event', 'vehicle_freeze', 'fog_of_war', 'battle_time_limit', 'min_tanks_per_division', 'max_tanks_per_division', 'division_cost', 'avg_clans_rating', 'avg_won_bet', 'avg_min_bet', 'min_vehicle_level', 'max_vehicle_level', 'available_extensions', 'provinces_count']], str] = ..., language: Literal['en'] = ..., limit: int = ..., page_no: int = ..., front_id: Union[str, List[str]] = ..., **kwargs) -> Any:
        """
        Method returns information about the Global Map Fronts.
        """
        ...

    async def wot_globalmap_provinces(self, region: str, front_id: str, fields: Union[Literal['arena_id', 'arena_name', 'daily_revenue', 'front_id', 'front_name', 'revenue_level', 'prime_time', 'province_id', 'province_name', 'landing_type', 'world_redivision', 'current_min_bet', 'last_won_bet', 'neighbours', 'uri', 'round_number', 'battles_start_at', 'status', 'max_bets', 'competitors', 'attackers', 'active_battles', 'owner_clan_id', 'is_borders_disabled', 'pillage_end_at', 'server'], List[Literal['arena_id', 'arena_name', 'daily_revenue', 'front_id', 'front_name', 'revenue_level', 'prime_time', 'province_id', 'province_name', 'landing_type', 'world_redivision', 'current_min_bet', 'last_won_bet', 'neighbours', 'uri', 'round_number', 'battles_start_at', 'status', 'max_bets', 'competitors', 'attackers', 'active_battles', 'owner_clan_id', 'is_borders_disabled', 'pillage_end_at', 'server']], str] = ..., language: Literal['en'] = ..., limit: int = ..., page_no: int = ..., prime_hour: int = ..., landing_type: Literal['null', 'auction', 'tournament'] = ..., arena_id: str = ..., daily_revenue_lte: int = ..., daily_revenue_gte: int = ..., order_by: Literal['province_id', '-province_id', 'daily_revenue', '-daily_revenue', 'prime_hour', '-prime_hour'] = ..., province_id: Union[str, List[str]] = ..., **kwargs) -> Any:
        """
        Method returns information about the Global Map provinces.
        """
        ...

    async def wot_globalmap_claninfo(self, region: str, clan_id: Union[int, List[int], str], fields: Union[Literal['clan_id', 'tag', 'name', 'statistics', 'ratings', 'private'], List[Literal['clan_id', 'tag', 'name', 'statistics', 'ratings', 'private']], str] = ..., access_token: str = ..., **kwargs) -> Any:
        """
        Method returns clan data on the Global Map.
        """
        ...

    async def wot_globalmap_clanprovinces(self, region: str, clan_id: Union[int, List[int], str], fields: Union[Literal['arena_id', 'arena_name', 'daily_revenue', 'front_id', 'front_name', 'revenue_level', 'prime_time', 'province_id', 'province_name', 'clan_id', 'landing_type', 'turns_owned', 'max_vehicle_level', 'private', 'pillage_end_at'], List[Literal['arena_id', 'arena_name', 'daily_revenue', 'front_id', 'front_name', 'revenue_level', 'prime_time', 'province_id', 'province_name', 'clan_id', 'landing_type', 'turns_owned', 'max_vehicle_level', 'private', 'pillage_end_at']], str] = ..., access_token: str = ..., language: Literal['en'] = ..., **kwargs) -> Any:
        """
        Method returns lists of clans provinces.
        """
        ...

    async def wot_globalmap_clanbattles(self, region: str, clan_id: int, fields: Union[Literal['front_id', 'front_name', 'province_id', 'province_name', 'time', 'type', 'competitor_id', 'attack_type', 'vehicle_level'], List[Literal['front_id', 'front_name', 'province_id', 'province_name', 'time', 'type', 'competitor_id', 'attack_type', 'vehicle_level']], str] = ..., language: Literal['en'] = ..., limit: int = ..., page_no: int = ..., **kwargs) -> Any:
        """
        Method returns list of clan's battles on the Global Map.
        """
        ...

    async def wot_globalmap_seasons(self, region: str, fields: Union[Literal['season_id', 'season_name', 'start', 'end', 'status', 'fronts'], List[Literal['season_id', 'season_name', 'start', 'end', 'status', 'fronts']], str] = ..., language: Literal['en'] = ..., page_no: int = ..., season_id: str = ..., limit: int = ..., status: Literal['PLANNED', 'ACTIVE', 'FINISHED'] = ..., **kwargs) -> Any:
        """
        Method returns information about seasons.
        """
        ...

    async def wot_globalmap_seasonclaninfo(self, region: str, season_id: str, vehicle_level: Union[Literal['6', '8', '10'], List[Literal['6', '8', '10']]], clan_id: int, fields: Union[Literal['seasons'], List[Literal['seasons']], str] = ..., **kwargs) -> Any:
        """
        Method returns clan's statistics for a specific season.
        """
        ...

    async def wot_globalmap_seasonaccountinfo(self, region: str, season_id: str, vehicle_level: Union[Literal['6', '8', '10'], List[Literal['6', '8', '10']]], account_id: int, fields: Union[Literal['seasons'], List[Literal['seasons']], str] = ..., **kwargs) -> Any:
        """
        Method returns player's statistics for a specific season.
        """
        ...

    async def wot_globalmap_seasonrating(self, region: str, season_id: str, vehicle_level: Literal['6', '8', '10'], fields: Union[Literal['clan_id', 'name', 'tag', 'color', 'award_level', 'rank', 'rank_delta', 'updated_at', 'victory_points', 'victory_points_to_next_award'], List[Literal['clan_id', 'name', 'tag', 'color', 'award_level', 'rank', 'rank_delta', 'updated_at', 'victory_points', 'victory_points_to_next_award']], str] = ..., page_no: int = ..., limit: int = ..., **kwargs) -> Any:
        """
        Method returns season clan rating.
        """
        ...

    async def wot_globalmap_seasonratingneighbors(self, region: str, season_id: str, vehicle_level: Literal['6', '8', '10'], clan_id: int, fields: Union[Literal['clan_id', 'name', 'tag', 'color', 'award_level', 'rank', 'rank_delta', 'updated_at', 'victory_points', 'victory_points_to_next_award'], List[Literal['clan_id', 'name', 'tag', 'color', 'award_level', 'rank', 'rank_delta', 'updated_at', 'victory_points', 'victory_points_to_next_award']], str] = ..., limit: int = ..., **kwargs) -> Any:
        """
        Method returns list of adjacent positions in season clan rating.
        """
        ...

    async def wot_globalmap_events(self, region: str, fields: Union[Literal['event_id', 'event_name', 'start', 'end', 'status', 'fronts'], List[Literal['event_id', 'event_name', 'start', 'end', 'status', 'fronts']], str] = ..., language: Literal['en'] = ..., page_no: int = ..., event_id: str = ..., limit: int = ..., status: Literal['PLANNED', 'ACTIVE', 'FINISHED'] = ..., **kwargs) -> Any:
        """
        Method returns events information.
        """
        ...

    async def wot_globalmap_eventclaninfo(self, region: str, event_id: str, front_id: Union[str, List[str]], clan_id: int, fields: Union[Literal['events'], List[Literal['events']], str] = ..., **kwargs) -> Any:
        """
        Method returns clan's statistics for a specific event.
        """
        ...

    async def wot_globalmap_eventclantasks(self, region: str, clan_id: int, event_id: str, fields: Union[Literal['event_id', 'clan_id', 'province_id', 'province_name', 'front_id', 'front_name', 'url', 'task_id', 'task_name', 'status', 'created_at', 'updated_at'], List[Literal['event_id', 'clan_id', 'province_id', 'province_name', 'front_id', 'front_name', 'url', 'task_id', 'task_name', 'status', 'created_at', 'updated_at']], str] = ..., language: Literal['en'] = ..., page_no: int = ..., limit: int = ..., **kwargs) -> Any:
        """
        Method returns clan's missions for a specific event.
        """
        ...

    async def wot_globalmap_eventaccountinfo(self, region: str, event_id: str, front_id: Union[str, List[str]], account_id: int, fields: Union[Literal['events'], List[Literal['events']], str] = ..., clan_id: int = ..., **kwargs) -> Any:
        """
        Method returns player's statistics for a specific event
        """
        ...

    async def wot_globalmap_eventaccountratings(self, region: str, event_id: str, front_id: str, fields: Union[Literal['event_id', 'account_id', 'clan_id', 'clan_rank', 'battles', 'battles_to_award', 'award_level', 'updated_at', 'fame_points', 'fame_points_to_improve_award', 'front_id', 'url', 'rank', 'rank_delta'], List[Literal['event_id', 'account_id', 'clan_id', 'clan_rank', 'battles', 'battles_to_award', 'award_level', 'updated_at', 'fame_points', 'fame_points_to_improve_award', 'front_id', 'url', 'rank', 'rank_delta']], str] = ..., page_no: int = ..., limit: int = ..., in_rating: Literal['1', '0'] = ..., **kwargs) -> Any:
        """
        Method returns account event rating.
        """
        ...

    async def wot_globalmap_eventaccountratingneighbors(self, region: str, event_id: str, front_id: str, account_id: int, fields: Union[Literal['event_id', 'account_id', 'clan_id', 'clan_rank', 'battles', 'battles_to_award', 'award_level', 'updated_at', 'fame_points', 'fame_points_to_improve_award', 'front_id', 'url', 'rank', 'rank_delta'], List[Literal['event_id', 'account_id', 'clan_id', 'clan_rank', 'battles', 'battles_to_award', 'award_level', 'updated_at', 'fame_points', 'fame_points_to_improve_award', 'front_id', 'url', 'rank', 'rank_delta']], str] = ..., page_no: int = ..., limit: int = ..., neighbours_count: int = ..., **kwargs) -> Any:
        """
        Method returns adjacent position in account event rating.
        """
        ...

    async def wot_globalmap_eventrating(self, region: str, event_id: str, front_id: str, fields: Union[Literal['clan_id', 'name', 'tag', 'color', 'award_level', 'rank', 'rank_delta', 'updated_at', 'battle_fame_points', 'total_fame_points', 'task_fame_points', 'fame_points_to_improve_award'], List[Literal['clan_id', 'name', 'tag', 'color', 'award_level', 'rank', 'rank_delta', 'updated_at', 'battle_fame_points', 'total_fame_points', 'task_fame_points', 'fame_points_to_improve_award']], str] = ..., page_no: int = ..., limit: int = ..., **kwargs) -> Any:
        """
        Method returns event clan rating
        """
        ...

    async def wot_globalmap_eventratingneighbors(self, region: str, event_id: str, front_id: str, clan_id: int, fields: Union[Literal['clan_id', 'name', 'tag', 'color', 'award_level', 'rank', 'rank_delta', 'updated_at', 'battle_fame_points', 'total_fame_points', 'task_fame_points', 'fame_points_to_improve_award'], List[Literal['clan_id', 'name', 'tag', 'color', 'award_level', 'rank', 'rank_delta', 'updated_at', 'battle_fame_points', 'total_fame_points', 'task_fame_points', 'fame_points_to_improve_award']], str] = ..., limit: int = ..., **kwargs) -> Any:
        """
        Method returns list of adjacent positions in event clan rating
        """
        ...

    async def wot_globalmap_info(self, region: str, fields: Union[Literal['state', 'last_turn', 'last_turn_created_at', 'last_turn_calculated_at'], List[Literal['state', 'last_turn', 'last_turn_created_at', 'last_turn_calculated_at']], str] = ..., **kwargs) -> Any:
        """
        Method returns general information about the Global Map.
        """
        ...

    async def wot_encyclopedia_tanks(self, region: str, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['name', 'name_i18n', 'nation', 'nation_i18n', 'level', 'tank_id', 'is_premium', 'type', 'type_i18n', 'short_name_i18n', 'image', 'image_small', 'contour_image'], List[Literal['name', 'name_i18n', 'nation', 'nation_i18n', 'level', 'tank_id', 'is_premium', 'type', 'type_i18n', 'short_name_i18n', 'image', 'image_small', 'contour_image']], str] = ..., **kwargs) -> Any:
        """
        Method returns list of all vehicles from Tankopedia.
        """
        ...

    async def wot_encyclopedia_tankinfo(self, region: str, tank_id: Union[int, List[int], str], language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['name', 'name_i18n', 'nation', 'nation_i18n', 'level', 'price_gold', 'price_credit', 'tank_id', 'localized_name', 'short_name_i18n', 'image', 'image_small', 'contour_image', 'max_health', 'limit_weight', 'is_gift', 'crew', 'engine_power', 'speed_limit', 'chassis_rotation_speed', 'turret_rotation_speed', 'vehicle_armor_forehead', 'vehicle_armor_board', 'vehicle_armor_fedd', 'turret_armor_forehead', 'turret_armor_board', 'turret_armor_fedd', 'gun_name', 'gun_max_ammo', 'gun_damage_min', 'gun_damage_max', 'gun_piercing_power_min', 'gun_piercing_power_max', 'gun_rate', 'circular_vision_radius', 'radio_distance', 'turrets', 'guns', 'engines', 'chassis', 'radios', 'type', 'type_i18n', 'is_premium', 'parent_tanks', 'weight', 'price_xp'], List[Literal['name', 'name_i18n', 'nation', 'nation_i18n', 'level', 'price_gold', 'price_credit', 'tank_id', 'localized_name', 'short_name_i18n', 'image', 'image_small', 'contour_image', 'max_health', 'limit_weight', 'is_gift', 'crew', 'engine_power', 'speed_limit', 'chassis_rotation_speed', 'turret_rotation_speed', 'vehicle_armor_forehead', 'vehicle_armor_board', 'vehicle_armor_fedd', 'turret_armor_forehead', 'turret_armor_board', 'turret_armor_fedd', 'gun_name', 'gun_max_ammo', 'gun_damage_min', 'gun_damage_max', 'gun_piercing_power_min', 'gun_piercing_power_max', 'gun_rate', 'circular_vision_radius', 'radio_distance', 'turrets', 'guns', 'engines', 'chassis', 'radios', 'type', 'type_i18n', 'is_premium', 'parent_tanks', 'weight', 'price_xp']], str] = ..., **kwargs) -> Any:
        """
        Method returns vehicle details from Tankopedia.
        """
        ...

    async def wot_encyclopedia_vehicles(self, region: str, fields: Union[Literal['tank_id', 'type', 'tag', 'name', 'short_name', 'description', 'nation', 'tier', 'is_premium', 'is_gift', 'is_wheeled', 'is_premium_igr', 'images', 'price_credit', 'price_gold', 'prices_xp', 'next_tanks', 'default_profile', 'guns', 'turrets', 'engines', 'suspensions', 'radios', 'provisions', 'modules_tree', 'crew', 'multination'], List[Literal['tank_id', 'type', 'tag', 'name', 'short_name', 'description', 'nation', 'tier', 'is_premium', 'is_gift', 'is_wheeled', 'is_premium_igr', 'images', 'price_credit', 'price_gold', 'prices_xp', 'next_tanks', 'default_profile', 'guns', 'turrets', 'engines', 'suspensions', 'radios', 'provisions', 'modules_tree', 'crew', 'multination']], str] = ..., language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., page_no: int = ..., limit: int = ..., tank_id: Union[int, List[int], str] = ..., nation: Union[str, List[str]] = ..., type: Union[Literal['heavyTank', 'AT-SPG', 'mediumTank', 'lightTank', 'SPG'], List[Literal['heavyTank', 'AT-SPG', 'mediumTank', 'lightTank', 'SPG']]] = ..., tier: Union[int, List[int], str] = ..., **kwargs) -> Any:
        """
        Method returns list of available vehicles.
        """
        ...

    async def wot_encyclopedia_vehicleprofile(self, region: str, tank_id: int, fields: Union[Literal['hp', 'hull_hp', 'weight', 'hull_weight', 'max_weight', 'max_ammo', 'speed_forward', 'speed_backward', 'modules', 'armor', 'engine', 'gun', 'turret', 'suspension', 'radio', 'ammo', 'siege', 'rapid', 'tank_id', 'is_default', 'profile_id'], List[Literal['hp', 'hull_hp', 'weight', 'hull_weight', 'max_weight', 'max_ammo', 'speed_forward', 'speed_backward', 'modules', 'armor', 'engine', 'gun', 'turret', 'suspension', 'radio', 'ammo', 'siege', 'rapid', 'tank_id', 'is_default', 'profile_id']], str] = ..., language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., engine_id: int = ..., gun_id: int = ..., suspension_id: int = ..., turret_id: int = ..., radio_id: int = ..., profile_id: str = ..., **kwargs) -> Any:
        """
        Method returns vehicle configuration characteristics based on the specified module IDs.
        """
        ...

    async def wot_encyclopedia_vehicleprofiles(self, region: str, tank_id: int, fields: Union[Literal['profile_id', 'tank_id', 'is_default', 'price_credit'], List[Literal['profile_id', 'tank_id', 'is_default', 'price_credit']], str] = ..., language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., order_by: Literal['price_credit', '-price_credit'] = ..., **kwargs) -> Any:
        """
        Method returns vehicle configuration characteristics.
        """
        ...

    async def wot_encyclopedia_tankengines(self, region: str, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['name', 'name_i18n', 'nation', 'nation_i18n', 'level', 'price_gold', 'price_credit', 'module_id', 'power', 'fire_starting_chance', 'tanks'], List[Literal['name', 'name_i18n', 'nation', 'nation_i18n', 'level', 'price_gold', 'price_credit', 'module_id', 'power', 'fire_starting_chance', 'tanks']], str] = ..., module_id: Union[int, List[int], str] = ..., nation: Union[str, List[str]] = ..., **kwargs) -> Any:
        """
        Method returns list of engines.
        """
        ...

    async def wot_encyclopedia_tankturrets(self, region: str, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['name', 'name_i18n', 'nation', 'nation_i18n', 'level', 'price_gold', 'price_credit', 'module_id', 'armor_forehead', 'armor_board', 'armor_fedd', 'rotation_speed', 'circular_vision_radius', 'tanks'], List[Literal['name', 'name_i18n', 'nation', 'nation_i18n', 'level', 'price_gold', 'price_credit', 'module_id', 'armor_forehead', 'armor_board', 'armor_fedd', 'rotation_speed', 'circular_vision_radius', 'tanks']], str] = ..., module_id: Union[int, List[int], str] = ..., nation: Union[str, List[str]] = ..., **kwargs) -> Any:
        """
        Method returns list of turrets.
        """
        ...

    async def wot_encyclopedia_tankradios(self, region: str, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['name', 'name_i18n', 'nation', 'nation_i18n', 'level', 'price_gold', 'price_credit', 'module_id', 'distance', 'tanks'], List[Literal['name', 'name_i18n', 'nation', 'nation_i18n', 'level', 'price_gold', 'price_credit', 'module_id', 'distance', 'tanks']], str] = ..., module_id: Union[int, List[int], str] = ..., nation: Union[str, List[str]] = ..., **kwargs) -> Any:
        """
        Method returns list of radios.
        """
        ...

    async def wot_encyclopedia_tankchassis(self, region: str, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['name', 'name_i18n', 'nation', 'nation_i18n', 'level', 'price_gold', 'price_credit', 'module_id', 'max_load', 'rotation_speed', 'tanks'], List[Literal['name', 'name_i18n', 'nation', 'nation_i18n', 'level', 'price_gold', 'price_credit', 'module_id', 'max_load', 'rotation_speed', 'tanks']], str] = ..., module_id: Union[int, List[int], str] = ..., nation: Union[str, List[str]] = ..., **kwargs) -> Any:
        """
        Method returns list of suspensions.
        """
        ...

    async def wot_encyclopedia_tankguns(self, region: str, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['name', 'name_i18n', 'nation', 'nation_i18n', 'level', 'price_gold', 'price_credit', 'module_id', 'damage', 'piercing_power', 'rate', 'turrets', 'tanks'], List[Literal['name', 'name_i18n', 'nation', 'nation_i18n', 'level', 'price_gold', 'price_credit', 'module_id', 'damage', 'piercing_power', 'rate', 'turrets', 'tanks']], str] = ..., module_id: Union[int, List[int], str] = ..., nation: Union[str, List[str]] = ..., turret_id: int = ..., tank_id: int = ..., **kwargs) -> Any:
        """
        Method returns a tanks' gun list.
        
        The logic of this method and some field values may vary according to optional parameters passed.
        
        Changeable fields:
        
         * **damage**
         * **piercing_power**
         * **rate**
         * **price_credit**
         * **price_gold**
        
        Optional input parameters work as follows:
        
         * correct **turret_id** passed — tank guns are filtered by whether they are placed on the turret and the abovementioned values change according to the turret;
         * correct **turret_id** and **module_id** passed — the method returns details on each module with the abovementioned values changed according to the turret, or returns null if the module is not compatible with the turret;
         * correct **tank_id** passed — if tank type matches one of AT-SPG, SPG, mediumTank, tank guns are filtered by whether they belong to the tank, the abovementioned values change according to the tank; otherwise, returns an error and requests **turret_id**. If **module_id** is also passed, the method returns details on each module with the abovementioned values changed according to the tank, or returns null if the module is not compatible with the tank;
         * compatible **turret_id** and **tank_id** passed — tank guns are filtered by whether they belong to the tank and are placed on the turret, the abovementioned values changed according to the turret.
        
        """
        ...

    async def wot_encyclopedia_achievements(self, region: str, fields: Union[Literal['name', 'name_i18n', 'type', 'section', 'section_order', 'image', 'image_big', 'description', 'condition', 'hero_info', 'order', 'options', 'outdated'], List[Literal['name', 'name_i18n', 'type', 'section', 'section_order', 'image', 'image_big', 'description', 'condition', 'hero_info', 'order', 'options', 'outdated']], str] = ..., language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., **kwargs) -> Any:
        """
        Method returns information about achievements.
        """
        ...

    async def wot_encyclopedia_info(self, region: str, fields: Union[Literal['game_version', 'tanks_updated_at', 'vehicle_types', 'vehicle_nations', 'vehicle_crew_roles', 'languages', 'achievement_sections'], List[Literal['game_version', 'tanks_updated_at', 'vehicle_types', 'vehicle_nations', 'vehicle_crew_roles', 'languages', 'achievement_sections']], str] = ..., language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., **kwargs) -> Any:
        """
        Method returns information about Tankopedia.
        """
        ...

    async def wot_encyclopedia_arenas(self, region: str, fields: Union[Literal['arena_id', 'camouflage_type', 'name_i18n', 'description'], List[Literal['arena_id', 'camouflage_type', 'name_i18n', 'description']], str] = ..., language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., **kwargs) -> Any:
        """
        Method returns information about maps.
        """
        ...

    async def wot_encyclopedia_provisions(self, region: str, fields: Union[Literal['provision_id', 'name', 'tag', 'price_gold', 'price_credit', 'type', 'description', 'weight', 'image'], List[Literal['provision_id', 'name', 'tag', 'price_gold', 'price_credit', 'type', 'description', 'weight', 'image']], str] = ..., language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., page_no: int = ..., limit: int = ..., type: Union[Literal['equipment', 'optionalDevice'], List[Literal['equipment', 'optionalDevice']]] = ..., provision_id: Union[int, List[int], str] = ..., **kwargs) -> Any:
        """
        Method returns a list of available equipment and consumables.
        """
        ...

    async def wot_encyclopedia_personalmissions(self, region: str, fields: Union[Literal['campaign_id', 'name', 'description', 'operations'], List[Literal['campaign_id', 'name', 'description', 'operations']], str] = ..., language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., campaign_id: Union[int, List[int], str] = ..., operation_id: Union[int, List[int], str] = ..., set_id: Union[int, List[int], str] = ..., tag: Union[str, List[str]] = ..., **kwargs) -> Any:
        """
        Method returns details on Personal Missions on the basis of specified campaign IDs, operation IDs, mission branch and tag IDs.
        """
        ...

    async def wot_encyclopedia_boosters(self, region: str, fields: Union[Literal['booster_id', 'name', 'description', 'images', 'lifetime', 'resource', 'is_auto', 'expires_at', 'price_credit', 'price_gold'], List[Literal['booster_id', 'name', 'description', 'images', 'lifetime', 'resource', 'is_auto', 'expires_at', 'price_credit', 'price_gold']], str] = ..., language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., **kwargs) -> Any:
        """
        Method returns information about Personal Reserves.
        """
        ...

    async def wot_encyclopedia_modules(self, region: str, fields: Union[Literal['module_id', 'type', 'name', 'price_credit', 'image', 'weight', 'tier', 'nation', 'tanks', 'default_profile'], List[Literal['module_id', 'type', 'name', 'price_credit', 'image', 'weight', 'tier', 'nation', 'tanks', 'default_profile']], str] = ..., extra: Union[Literal['default_profile'], List[Literal['default_profile']]] = ..., language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., page_no: int = ..., limit: int = ..., module_id: Union[int, List[int], str] = ..., type: Union[Literal['vehicleRadio', 'vehicleEngine', 'vehicleGun', 'vehicleChassis', 'vehicleTurret'], List[Literal['vehicleRadio', 'vehicleEngine', 'vehicleGun', 'vehicleChassis', 'vehicleTurret']]] = ..., nation: Union[str, List[str]] = ..., **kwargs) -> Any:
        """
        Method returns list of available modules that can be installed on vehicles, such as engines, turrets, etc. At least one input filter parameter (module ID, type) is required to be indicated.
        """
        ...

    async def wot_encyclopedia_badges(self, region: str, fields: Union[Literal['badge_id', 'name', 'description', 'images'], List[Literal['badge_id', 'name', 'description', 'images']], str] = ..., language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., **kwargs) -> Any:
        """
        Method returns list of available badges a player can gain in Ranked Battles.
        """
        ...

    async def wot_encyclopedia_crewroles(self, region: str, fields: Union[Literal['role', 'name', 'skills'], List[Literal['role', 'name', 'skills']], str] = ..., language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., role: Union[str, List[str]] = ..., **kwargs) -> Any:
        """
        Method returns full description of all crew qualifications.
        """
        ...

    async def wot_encyclopedia_crewskills(self, region: str, fields: Union[Literal['skill', 'name', 'description', 'image_url', 'is_perk'], List[Literal['skill', 'name', 'description', 'image_url', 'is_perk']], str] = ..., language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., skill: Union[str, List[str]] = ..., role: str = ..., **kwargs) -> Any:
        """
        Method returns full description of all crew skills.
        """
        ...

    async def wot_ratings_types(self, region: str, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['type', 'threshold', 'rank_fields'], List[Literal['type', 'threshold', 'rank_fields']], str] = ..., battle_type: Literal['company', 'random', 'team', 'default'] = ..., **kwargs) -> Any:
        """
        Method returns dictionary of rating periods and ratings details.
        """
        ...

    async def wot_ratings_dates(self, region: str, type: str, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['dates'], List[Literal['dates']], str] = ..., battle_type: Literal['company', 'random', 'team', 'default'] = ..., account_id: Union[int, List[int], str] = ..., **kwargs) -> Any:
        """
        Method returns dates with available rating data.
        """
        ...

    async def wot_ratings_accounts(self, region: str, type: str, account_id: Union[int, List[int], str], language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['account_id', 'battles_to_play', 'battles_count', 'capture_points', 'damage_avg', 'damage_dealt', 'frags_avg', 'frags_count', 'global_rating', 'hits_ratio', 'spotted_avg', 'spotted_count', 'survived_ratio', 'wins_ratio', 'xp_amount', 'xp_avg', 'xp_max'], List[Literal['account_id', 'battles_to_play', 'battles_count', 'capture_points', 'damage_avg', 'damage_dealt', 'frags_avg', 'frags_count', 'global_rating', 'hits_ratio', 'spotted_avg', 'spotted_count', 'survived_ratio', 'wins_ratio', 'xp_amount', 'xp_avg', 'xp_max']], str] = ..., battle_type: Literal['company', 'random', 'team', 'default'] = ..., date: Any = ..., **kwargs) -> Any:
        """
        Method returns player ratings by specified IDs.
        """
        ...

    async def wot_ratings_neighbors(self, region: str, type: str, account_id: int, rank_field: str, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['account_id', 'battles_to_play', 'battles_count', 'capture_points', 'damage_avg', 'damage_dealt', 'frags_avg', 'frags_count', 'global_rating', 'hits_ratio', 'spotted_avg', 'spotted_count', 'survived_ratio', 'wins_ratio', 'xp_amount', 'xp_avg', 'xp_max'], List[Literal['account_id', 'battles_to_play', 'battles_count', 'capture_points', 'damage_avg', 'damage_dealt', 'frags_avg', 'frags_count', 'global_rating', 'hits_ratio', 'spotted_avg', 'spotted_count', 'survived_ratio', 'wins_ratio', 'xp_amount', 'xp_avg', 'xp_max']], str] = ..., battle_type: Literal['company', 'random', 'team', 'default'] = ..., date: Any = ..., limit: int = ..., **kwargs) -> Any:
        """
        Method returns list of adjacent positions in specified rating.
        """
        ...

    async def wot_ratings_top(self, region: str, type: str, rank_field: str, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['account_id', 'battles_to_play', 'battles_count', 'capture_points', 'damage_avg', 'damage_dealt', 'frags_avg', 'frags_count', 'global_rating', 'hits_ratio', 'spotted_avg', 'spotted_count', 'survived_ratio', 'wins_ratio', 'xp_amount', 'xp_avg', 'xp_max'], List[Literal['account_id', 'battles_to_play', 'battles_count', 'capture_points', 'damage_avg', 'damage_dealt', 'frags_avg', 'frags_count', 'global_rating', 'hits_ratio', 'spotted_avg', 'spotted_count', 'survived_ratio', 'wins_ratio', 'xp_amount', 'xp_avg', 'xp_max']], str] = ..., battle_type: Literal['company', 'random', 'team', 'default'] = ..., date: Any = ..., limit: int = ..., page_no: int = ..., **kwargs) -> Any:
        """
        Method returns list of top players by specified parameter.
        """
        ...

    async def wot_clanratings_types(self, region: str, **kwargs) -> Any:
        """
        Method returns details on ratings types and categories.
        """
        ...

    async def wot_clanratings_dates(self, region: str, limit: int = ..., **kwargs) -> Any:
        """
        Method returns dates with available rating data.
        """
        ...

    async def wot_clanratings_clans(self, region: str, clan_id: Union[int, List[int], str], language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['clan_id', 'clan_name', 'clan_tag', 'v10l_avg', 'battles_count_avg', 'battles_count_avg_daily', 'global_rating_avg', 'global_rating_weighted_avg', 'efficiency', 'wins_ratio_avg', 'rating_fort', 'fb_elo_rating', 'fb_elo_rating_10', 'fb_elo_rating_8', 'fb_elo_rating_6', 'gm_elo_rating', 'gm_elo_rating_10', 'gm_elo_rating_8', 'gm_elo_rating_6', 'exclude_reasons'], List[Literal['clan_id', 'clan_name', 'clan_tag', 'v10l_avg', 'battles_count_avg', 'battles_count_avg_daily', 'global_rating_avg', 'global_rating_weighted_avg', 'efficiency', 'wins_ratio_avg', 'rating_fort', 'fb_elo_rating', 'fb_elo_rating_10', 'fb_elo_rating_8', 'fb_elo_rating_6', 'gm_elo_rating', 'gm_elo_rating_10', 'gm_elo_rating_8', 'gm_elo_rating_6', 'exclude_reasons']], str] = ..., date: Any = ..., **kwargs) -> Any:
        """
        Method returns clan ratings by specified IDs.
        """
        ...

    async def wot_clanratings_neighbors(self, region: str, rank_field: str, clan_id: int, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['clan_id', 'clan_name', 'clan_tag', 'v10l_avg', 'battles_count_avg', 'battles_count_avg_daily', 'global_rating_avg', 'global_rating_weighted_avg', 'efficiency', 'wins_ratio_avg', 'rating_fort', 'fb_elo_rating', 'fb_elo_rating_10', 'fb_elo_rating_8', 'fb_elo_rating_6', 'gm_elo_rating', 'gm_elo_rating_10', 'gm_elo_rating_8', 'gm_elo_rating_6', 'exclude_reasons'], List[Literal['clan_id', 'clan_name', 'clan_tag', 'v10l_avg', 'battles_count_avg', 'battles_count_avg_daily', 'global_rating_avg', 'global_rating_weighted_avg', 'efficiency', 'wins_ratio_avg', 'rating_fort', 'fb_elo_rating', 'fb_elo_rating_10', 'fb_elo_rating_8', 'fb_elo_rating_6', 'gm_elo_rating', 'gm_elo_rating_10', 'gm_elo_rating_8', 'gm_elo_rating_6', 'exclude_reasons']], str] = ..., date: Any = ..., limit: int = ..., **kwargs) -> Any:
        """
        Method returns list of adjacent positions in specified clan rating.
        """
        ...

    async def wot_clanratings_top(self, region: str, rank_field: str, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['clan_id', 'clan_name', 'clan_tag', 'v10l_avg', 'battles_count_avg', 'battles_count_avg_daily', 'global_rating_avg', 'global_rating_weighted_avg', 'efficiency', 'wins_ratio_avg', 'rating_fort', 'fb_elo_rating', 'fb_elo_rating_10', 'fb_elo_rating_8', 'fb_elo_rating_6', 'gm_elo_rating', 'gm_elo_rating_10', 'gm_elo_rating_8', 'gm_elo_rating_6', 'exclude_reasons'], List[Literal['clan_id', 'clan_name', 'clan_tag', 'v10l_avg', 'battles_count_avg', 'battles_count_avg_daily', 'global_rating_avg', 'global_rating_weighted_avg', 'efficiency', 'wins_ratio_avg', 'rating_fort', 'fb_elo_rating', 'fb_elo_rating_10', 'fb_elo_rating_8', 'fb_elo_rating_6', 'gm_elo_rating', 'gm_elo_rating_10', 'gm_elo_rating_8', 'gm_elo_rating_6', 'exclude_reasons']], str] = ..., date: Any = ..., page_no: int = ..., limit: int = ..., **kwargs) -> Any:
        """
        Method returns the list of top clans by specified parameters.
        """
        ...

    async def wot_tanks_stats(self, region: str, account_id: int, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['account_id', 'tank_id', 'all', 'company', 'stronghold_defense', 'stronghold_skirmish', 'clan', 'random', 'fallout', 'team', 'regular_team', 'globalmap', 'epic', 'ranked_battles', 'max_xp', 'max_frags', 'frags', 'in_garage', 'mark_of_mastery', 'ranked_10x10'], List[Literal['account_id', 'tank_id', 'all', 'company', 'stronghold_defense', 'stronghold_skirmish', 'clan', 'random', 'fallout', 'team', 'regular_team', 'globalmap', 'epic', 'ranked_battles', 'max_xp', 'max_frags', 'frags', 'in_garage', 'mark_of_mastery', 'ranked_10x10']], str] = ..., access_token: str = ..., extra: Union[Literal['epic', 'fallout', 'random', 'ranked_10x10', 'ranked_battles'], List[Literal['epic', 'fallout', 'random', 'ranked_10x10', 'ranked_battles']]] = ..., tank_id: Union[int, List[int], str] = ..., in_garage: Literal['1', '0'] = ..., **kwargs) -> Any:
        """
        Method returns overall statistics, Tank Company statistics, and clan statistics per each vehicle for each user.
        """
        ...

    async def wot_tanks_achievements(self, region: str, account_id: int, language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['account_id', 'tank_id', 'achievements', 'series', 'max_series'], List[Literal['account_id', 'tank_id', 'achievements', 'series', 'max_series']], str] = ..., access_token: str = ..., tank_id: Union[int, List[int], str] = ..., in_garage: Literal['1', '0'] = ..., **kwargs) -> Any:
        """
        Method returns list of achievements on all player's vehicles.
        
        Achievement properties define the **achievements** field values:
        
         * 1-4 for Mastery Badges and Stage Achievements (type: "class");
         * maximum value of Achievement series (type: "series");
         * number of achievements earned from sections: Battle Hero, Epic Achievements, Group Achievements, Special Achievements, etc. (type: "repeatable, single, custom").
        
        """
        ...

    async def wot_tanks_mastery(self, region: str, distribution: Literal['damage', 'xp'], percentile: Union[int, List[int], str], language: Literal['en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'zh-tw', 'tr', 'cs', 'th', 'vi', 'ko'] = ..., fields: Union[Literal['distribution', 'updated_at'], List[Literal['distribution', 'updated_at']], str] = ..., tank_id: Union[int, List[int], str] = ..., **kwargs) -> Any:
        """
        The method returns percentiles of the distribution of average damage or experience values for each piece of equipment
        """
        ...
