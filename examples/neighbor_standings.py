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
        user_classic_leagues = user.leagues['classic']
        user_rank, rank_sort = await user.get_rank_in_classic_league(314, include_rank_sort=True)
        print('user_rank', user_rank)
        # get corresponding page range for given entry rank and delta
        league = await fpl.get_classic_league(league_id)
        a = await league.get_rank_neighbors(user_rank, rank_sort, delta=delta)
        print(user.name)
        print(a)





# def get_element_ownership_in_league(league_id=None, event_id=None, num_entries=None, bin_size=None,
#                                     bin_sample_size=None, json_entries=None, dest_filepath=None,
#                                     league_type=None, debug=None, start_page=1):
#     # TODO
#     # Defaults
#     if league_id is None:
#         league_id = 314
#     if event_id is None:
#         event_id = 1
#     if num_entries is None:
#         num_entries = 50
#     if bin_size is None:
#         bin_size = 1
#     if bin_sample_size is None:
#         bin_sample_size = 1

#     if bin_sample_size > bin_size:
#         raise Exception(f'bin_size must be greater than bin_sample_size')

#     num_bins = math.ceil(num_entries / bin_size)
#     num_pages = num_entries // ENTRIES_PER_PAGE + 1
#     mod = num_entries % ENTRIES_PER_PAGE

#     if debug:
#         logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

#     # getPlayersInfo()
#     main = get_main()
#     element_id_to_name = get_map_of_list(
#         main['elements'], lambda el: el['id'], lambda el: f"{el['first_name']} {el['second_name']}")

#     binned_idx_samples = get_sampled_bins(
#         bin_size, num_bins, bin_sample_size)

#     if league_type == "h2h":
#         standings = []
#         return
#     else:
#         standings = get_n_top_entries_in_league(league_id, num_entries)

#     sampled_standings = [standings[i] for i in [
#         item for sublist in binned_idx_samples for item in sublist]]

#     binned_element_picks_ct = [{} for _ in range(num_bins)]

#     for i, entry in enumerate(sampled_standings):
#         entry_id = entry['entry']
#         bin_idx = i // bin_sample_size
#         entry_picks = get_entry_picks(entry_id, event_id)['picks']
#         picks_element_ids = [pick['element'] for pick in entry_picks]
#         pick_cts = Counter(picks_element_ids)
#         for k, ct in pick_cts.items():
#             if element_id_to_name[k] in binned_element_picks_ct[bin_idx]:
#                 binned_element_picks_ct[bin_idx][element_id_to_name[k]] += ct
#             else:
#                 binned_element_picks_ct[bin_idx][element_id_to_name[k]] = ct
#     return binned_element_picks_ct

asyncio.run(get_entry_neighbors_in_classic_league(141176, 314, 3))