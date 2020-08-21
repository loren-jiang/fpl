import math
import sys
import logging
import aiohttp
import asyncio
import json
import os

from fpl.constants import ENTRIES_PER_PAGE
from fpl import FPL
from collections import Counter, defaultdict

async def get_top_n_entries(league_id=314, n=10000):
    """Gets top 10k entries in `Overall` league

    Args:
        league_id (int, optional): [description]. Defaults to 314.
    """
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        # get corresponding page range for given entry rank and delta
        league = await fpl.get_classic_league(league_id)
        out = await league.get_top_rank_users(n)
        with open(f'test_data/top_{n}_entries.json', 'w') as f:
            f.write(json.dumps(out))
        return out

asyncio.run(get_top_n_entries(n=10))