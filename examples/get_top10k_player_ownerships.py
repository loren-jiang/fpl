import math
import sys
import logging
import aiohttp
import asyncio
import json
import os
import pymongo

from fpl.constants import ENTRIES_PER_PAGE, API_URLS
from fpl import FPL
from collections import Counter, defaultdict
from fpl.utils import create_bins, get_map_of_list, get_sampled_bins
from fpl.fpl import fetch

from pymongo import MongoClient, ReplaceOne, UpdateMany, UpdateOne
# from test_data import BS_STATC, TOP10K_ENTRIES
from datetime import datetime


client = MongoClient('localhost', 27017)
db = client.fpl


async def get_top_n_player_ownerships(league_id=314, event_id=1, num_entries=100, bin_size=100,
                                      bin_sample_size=25):
    async with aiohttp.ClientSession() as session:
        # fpl = FPL(session)
        # get corresponding page range for given entry rank and delta
        # league = await fpl.get_classic_league(league_id)
        # top_users = await league.get_top_rank_users(num_entries)
        # top_users_ids = [user['entry'] for user in top_users]

        top_users_ids = db.top10k.find_one({"gw": 38})['top10k']
        num_bins=math.ceil(num_entries / bin_size)

        binned_idx_samples=get_sampled_bins(
            bin_size, num_bins, bin_sample_size)
        sampled_standings=[top_users_ids[i] for i in [
            item for sublist in binned_idx_samples for item in sublist]]

        element_ct_bins={}

        for i, entry_id in enumerate(sampled_standings):
            bin_idx=i // bin_sample_size
            response=await fetch(session, API_URLS['user_picks'].format(entry_id, event_id))
            entry_picks=response['picks']
            picks_element_ids=[pick['element'] for pick in entry_picks]
            pick_cts=Counter(picks_element_ids)
            for k, ct in pick_cts.items():
                if k in element_ct_bins:
                    element_ct_bins[k][bin_idx] += ct
                else:
                    element_ct_bins[k]=[0]*num_bins


        return element_ct_bins


asyncio.run(get_top_n_player_ownerships())
