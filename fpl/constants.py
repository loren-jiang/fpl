API_BASE_URL = "https://fantasy.premierleague.com/api/"

API_URLS = {
    "dynamic": "{}bootstrap-dynamic/".format(API_BASE_URL),  # doesnt work
    "fixtures": "{}fixtures/".format(API_BASE_URL),
    "gameweeks": "{}events/".format(API_BASE_URL),  # doesnt work
    "gameweek_fixtures": "{}fixtures/?event={{}}".format(API_BASE_URL),
    "gameweek_live": "{}event/{{}}/live".format(API_BASE_URL),
    "league_classic": "{}leagues-classic/{{}}/standings/".format(API_BASE_URL),
    "league_classic_standings": "{}leagues-classic/{{}}/standings/?page_standings={{}}".format(API_BASE_URL),
    "league_h2h": "{}leagues-h2h/{{}}/standings/".format(API_BASE_URL),
    "league_h2h_fixtures": "{}leagues-h2h-matches/league/{{}}/?{{}}page={{}}".format(API_BASE_URL),
    "players": "{}elements/".format(API_BASE_URL),  # doesnt work
    "player": "{}element-summary/{{}}/".format(API_BASE_URL),
    "settings": "{}game-settings/".format(API_BASE_URL),  # doesnt work
    "static": "{}bootstrap-static/".format(API_BASE_URL),
    "teams": "{}teams/".format(API_BASE_URL), #doesnt work
    "transfers": "{}transfers/".format(API_BASE_URL),
    "user": "{}entry/{{}}/".format(API_BASE_URL),
    "user_cup": "{}entry/{{}}/cup/".format(API_BASE_URL),
    "user_history": "{}entry/{{}}/history/".format(API_BASE_URL),
    "user_picks": "{}entry/{{}}/event/{{}}/picks/".format(API_BASE_URL),
    "user_team": "{}my-team/{{}}/".format(API_BASE_URL),
    "user_transfers": "{}entry/{{}}/transfers/".format(API_BASE_URL),
    "user_latest_transfers": "{}entry/{{}}/transfers-latest/".format(
        API_BASE_URL),
    "watchlist": "{}watchlist/".format(API_BASE_URL),
    "me": "{}me/".format(API_BASE_URL)
}


SEASON_MAP = {
    '2020-21': ('09-12-2020', '05-23-2021'),
    "2019-20": ('08-09-2019', '07-26-2020'),
    "2018-19": ('08-10-2028', '05-12-2019'),
    "2017-18": ('08-11-2017', '05-13-2018'),
    "2016-17": ('08-13-2016', '05-21-2017'),
    "2015-16": ('08-08-2015', '05-17-2016'),
}


PICKS_FORMAT = "{} {}{}"
MYTEAM_FORMAT = "{}{}"

MIN_GAMEWEEK = 1
MAX_GAMEWEEK = 47
ENTRIES_PER_PAGE = 50
OVERALL_LEAGUE_ID = 314