import asyncio
import random
import math

from functools import update_wrapper

from fpl.constants import API_URLS

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13"}


async def fetch(session, url):
    async with session.get(url, headers=headers) as response:
        assert response.status == 200
        return await response.json()


# async def fetch(session, url):
#     while True:
#         try:
#             async with session.get(url, headers=headers) as response:
#                 assert response.status == 200
#                 return await response.json()
#         except Exception as e:
#             print(e)


async def post(session, url, payload, headers):
    async with session.post(url, data=payload, headers=headers) as response:
        return await response.json()


async def get_total_players(session):
    """Returns the total number of registered players.

    :param aiohttp.ClientSession session: A logged in user's session.
    :rtype: int
    """
    static = await fetch(
        session, "https://fantasy.premierleague.com/api/bootstrap-static/")

    return static["total_players"]


async def get_current_gameweek(session):
    """Returns the current gameweek.

    :param aiohttp.ClientSession session: A logged in user's session.
    :rtype: int
    """
    static = await fetch(
        session, "https://fantasy.premierleague.com/api/bootstrap-static/")

    current_gameweek = next(event for event in static["events"]
                            if event["is_current"])

    return current_gameweek["id"]


def team_converter(team_id):
    """Converts a team's ID to their actual name."""
    team_map = {
        1: "Arsenal",
        2: "Aston Villa",
        3: "Bournemouth",
        4: "Brighton",
        5: "Burnley",
        6: "Chelsea",
        7: "Crystal Palace",
        8: "Everton",
        9: "Leicester",
        10: "Liverpool",
        11: "Man City",
        12: "Man Utd",
        13: "Newcastle",
        14: "Norwich",
        15: "Sheffield Utd",
        16: "Southampton",
        17: "Spurs",
        18: "Watford",
        19: "West Ham",
        20: "Wolves",
        None: None
    }
    return team_map[team_id]


def short_name_converter(team_id):
    """Converts a team's ID to their short name."""
    short_name_map = {
        1: "ARS",
        2: "AVL",
        3: "BOU",
        4: "BHA",
        5: "BUR",
        6: "CHE",
        7: "CRY",
        8: "EVE",
        9: "LEI",
        10: "LIV",
        11: "MCI",
        12: "MUN",
        13: "NEW",
        14: "NOR",
        15: "SHU",
        16: "SOU",
        17: "TOT",
        18: "WAT",
        19: "WHU",
        20: "WOL",
        None: None
    }
    return short_name_map[team_id]


def position_converter(position):
    """Converts a player's `element_type` to their actual position."""
    position_map = {
        1: "Goalkeeper",
        2: "Defender",
        3: "Midfielder",
        4: "Forward"
    }
    return position_map[position]


def chip_converter(chip):
    """Converts a chip name to usable string."""
    chip_map = {
        "3xc": "TC",
        "wildcard": "WC",
        "bboost": "BB",
        "freehit": "FH"
    }
    return chip_map[chip]


def scale(value, upper, lower, min_, max_):
    """Scales value between upper and lower values, depending on the given
    minimun and maximum value.
    """
    numerator = ((lower - upper) * float((value - min_)))
    denominator = float((max_ - min_))
    return numerator / denominator + upper


def average(iterable):
    """Returns the average value of the iterable."""
    try:
        return sum(iterable) / float(len(iterable))
    except ZeroDivisionError:
        return 0.0


def logged_in(session):
    """Checks that the user is logged in within the session.

    :param session: http session
    :type session: aiohttp.ClientSession
    :return: True if user is logged in else False
    :rtype: bool
    """
    return "csrftoken" in session.cookie_jar.filter_cookies(
        "https://users.premierleague.com/")


def coroutine(func):
    func = asyncio.coroutine(func)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))
    return update_wrapper(wrapper, func)


def get_headers(referer):
    """Returns the headers needed for the transfer request."""
    return {
        "Content-Type": "application/json; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": referer
    }


def levenshtein_distance(s1, s2):
    """Returns Levenshtein distance of two strings.
    """
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(
                    1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


async def get_current_user(session):
    user = await fetch(session, API_URLS["me"])
    return user


def create_bins(lower_bound, width, quantity):
    """ create_bins returns an equal-width (distance) partitioning. 
        It returns an ascending list of tuples, representing the intervals.
        A tuple bins[i], i.e. (bins[i][0], bins[i][1])  with i > 0 
        and i < quantity, satisfies the following conditions:
            (1) bins[i][0] + width == bins[i][1]
            (2) bins[i-1][0] + width == bins[i][0] and
                bins[i-1][1] + width == bins[i][1]
    """

    bins = []
    for low in range(lower_bound,
                     lower_bound + quantity*width + 1, width):
        bins.append((low, low+width))
    return bins

# r is a tuple representing start and end
# num is the number of samples


def random_sample_range(r, num):
    ret = random.sample(list(range(r[0], r[1], 1)), num)
    ret.sort()
    return ret


def get_page_num(x, k=50):
    return math.ceil(x/k)


def add_bool_arg(parser, name, default=False):
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--' + name, dest=name, action='store_true')
    group.add_argument('--no-' + name, dest=name, action='store_false')
    parser.set_defaults(**{name: default})


def get_map_of_list(lst, k_fxn, v_fxn):
    mapped_lst = {}
    for elem in lst:
        key = k_fxn(elem)
        if key not in mapped_lst:
            mapped_lst[key] = v_fxn(elem)
        else:
            raise Exception(f'Key function returned a non-unique key {key}. ')
    return mapped_lst


def get_bin_map(bins, bin_sample_size):
    entry_samples = [0] * len(bins)
    for i, x in enumerate(bins):
        samps = random_sample_range(x, bin_sample_size)
        entry_samples[i] = samps

    return entry_samples


def get_sampled_bins(bin_size, num_bins, bin_sample_size):
    bins = create_bins(0, bin_size, num_bins - 1)
    return get_bin_map(bins, bin_sample_size)
