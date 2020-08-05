import asyncio
from ..constants import API_URLS, ENTRIES_PER_PAGE
from ..utils import fetch

class ClassicLeague():
    """A class representing a classic league in the Fantasy Premier League.

    Basic usage::

      >>> from fpl import FPL
      >>> import aiohttp
      >>> import asyncio
      >>>
      >>> async def main():
      ...     async with aiohttp.ClientSession() as session:
      ...         fpl = FPL(session)
      ...         await fpl.login()
      ...         classic_league = await fpl.get_classic_league(1137)
      ...     print(classic_league)
      ...
      >>> asyncio.run(main())
      Official /r/FantasyPL Classic League - 1137
    """
    def __init__(self, league_information, session):
        self._session = session

        for k, v in league_information.items():
            setattr(self, k, v)

    async def get_standings(self, page=1, page_new_entries=1, phase=1):
        """Returns the league's standings of the given page.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/leagues-classic/967/standings/?page_new_entries=1&page_standings=1&phase=1

        :param page: A page of the league's standings (default is 50 managers
            per page).
        :type page: string or int
        :rtype: dict
        """
        if hasattr(self, "standings") and self.standings["page"] == page:
            return self.standings

        url = "{}?page_new_entries={}&page_standings={}&phase={}".format(
                API_URLS["league_classic"].format(self.league["id"]),
                page_new_entries, page, phase)
        standings = await fetch(self._session, url)
        self.standings = standings["standings"]

        return standings["standings"]

    async def get_standings_in_page_range(self, start_page, end_page):
        """TODO

        Args:
            start_page ([type]): [description]
            end_page ([type]): [description]

        Returns:
            [type]: [description]
        """
        tasks = [asyncio.ensure_future(
                     self.get_standings(page))
                     for page in range(start_page, end_page + 1)]
        agg_standings = await asyncio.gather(*tasks)

        return agg_standings

    async def get_top_rank_users(self, n):
        """TODO

        Args:
            n ([type]): [description]

        Returns:
            [type]: [description]
        """
        start_page = 1
        end_page = n // ENTRIES_PER_PAGE + 1
        standings = await self.get_standings_in_page_range(start_page, end_page)
        users = []
        for standing in standings:
            users += standing['results']
        return users[:n]

    async def get_rank_neighbors(self, rank, rank_sort=None, delta=50):
        """TODO

        Args:
            rank ([type]): [description]
            delta (int, optional): [description]. Defaults to 50.
        """
        
        rank_page_in_league = rank // ENTRIES_PER_PAGE + 1
        page_delta = delta // ENTRIES_PER_PAGE + 1
        start_page = max(1, rank_page_in_league - page_delta)

        if rank_sort is None:
            end_page = rank_page_in_league + page_delta
            standings = await self.get_standings_in_page_range(start_page, end_page)
            users = []
            for standing in standings:
                users += standing['results']
            if len(users) == 0:
                raise Exception('Rank exceeds number of users in league.')
            rank_idx = next(i for i, user in enumerate(
                users) if user['rank'] == rank)
            return users[max(0, rank_idx-delta):min(len(users), rank_idx+delta+1)]
        else:
            if rank_sort < rank:
                raise Exception('rank sort must be greater or equal to rank.')
            all_users = []
            i = 0
            user_idx = 0
            rank_found = False
            while not rank_found:
                standings = await self.get_standings(start_page)
                users = standings['results']
                all_users += users
                if len(users) == 0:
                    break
                for user in users:                    
                    if user['rank'] == rank and user['rank_sort'] == rank_sort:
                        user_idx = i
                        rank_found = True
                        break
                    i += 1
                start_page += 1
            
            additional_pages = delta // ENTRIES_PER_PAGE + 1
            for page in range(start_page, start_page + additional_pages):
                standings = await self.get_standings(start_page)
                users = standings['results']
                all_users += users
                if len(users) == 0:
                    break
            return all_users[max(0, user_idx - delta):min(len(all_users), user_idx+delta)]


    def __str__(self):
        return f"{self.league['name']} - {self.league['id']}"
