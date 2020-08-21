import math
import sys
import logging
import aiohttp
import asyncio
from fpl import FPL
# from requests import HTTPError
from fpl.constants import ENTRIES_PER_PAGE
# from endpoints import get_entry, get_classic_standings, get_entry_picks, get_main
# from tqdm import tqdm
# from utils import create_bins, get_map_of_list, get_sampled_bins
from collections import Counter, defaultdict


async def get_entry_neighbors_in_classic_league(user_id, league_id, delta=50):
    """TODO

    Args:
        entry_id ([type]): [description]
        league_id ([type]): [description]
        delta (int, optional): [description]. Defaults to 50.

    Raises:
        Exception: [description]

    Returns:
        [type]: [description]
    """
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        user = await fpl.get_user(user_id)
        user_rank, rank_sort = await user.get_rank_in_classic_league(314, include_rank_sort=True)
        # get corresponding page range for given entry rank and delta
        league = await fpl.get_classic_league(league_id)
        out = await league.get_rank_neighbors(user_rank, rank_sort, delta=delta)
        print(out)
        return out


asyncio.run(get_entry_neighbors_in_classic_league(141176, 314, 3))