## mypackage\baskref_data_scraper.py

from datetime import datetime
from dataclasses import dataclass
from urllib import parse
from bs4 import BeautifulSoup
from mypackage.html_scraper import HTMLScraper

@dataclass
class BaskRefDataScraper(HTMLScraper):
    """Class for scraping & Parsing basketball-reference.com data"""

    # public functions

    def get_games_data(self, game_urls: list) -> list:
        """
        Scrapes the game data for all the game urls provided
        :game_urls: list of box score game urls from basketball reference
        :return: returns a list of dictionaries with game data
        """

        return [self._scrape_game_data(url) for url in game_urls]

    # Private Methods

    ## scraping functions

    def _scrape_game_data(self, game_url: str) -> dict:
        """
        Scrapes the game data for the given game web page.
        :game_url: a Basketball Reference URL to a game page
        :return: returns a dictionary of game data
        """

        game_data = self.scrape(game_url, self._parse_game_data)
        game_data["game_id"] = self._parse_game_id(game_url)
        game_data["game_url"] = game_url

        return game_data

    ## parsing functions

    def _parse_game_data(self, game_page: BeautifulSoup) -> dict:
        """
        Parses the game data for the given game web page.
        :game_url: a Basketball Reference URL to a game page
        :return: returns a dictionary of game data
        """

        # Team names
        home_team_fn, home_team_sn = self._parse_team_name(game_page, "home")
        away_team_fn, away_team_sn = self._parse_team_name(game_page, "away")

        # game meta data
        meta_data = self._parse_game_meta_data(game_page)

        # basic stats
        home_basic_dic = self._parse_basic_stats(
            game_page, "home", home_team_sn
        )

        away_basic_dic = self._parse_basic_stats(
            game_page, "away", away_team_sn
        )

        return {
            "home_team": home_team_sn,
            "away_team": away_team_sn,
            "home_team_full_name": home_team_fn,
            "away_team_full_name": away_team_fn,
            **meta_data,
            **home_basic_dic,
            **away_basic_dic,
        }

    def _parse_team_name(
        self, html: BeautifulSoup, team: str
    ) -> tuple[str, str]:
        """
        Provided the BR game page and the team parameter it parses out
        the team short and long names.
        :team: indicates the home or away team
        :return: Tuple(team long name, team short name)
        """

        if team not in ["home", "away"]:
            raise ValueError('The team argument can only be "home" or "away"')

        team_idx = 2 if team == "home" else 1

        team_anchor = html.select_one(
            f"#content > div.scorebox > div:nth-child({team_idx}) "
            "> div:nth-child(1) > strong > a"
        )

        return team_anchor.text, team_anchor.attrs["href"].split("/")[2]

    def _parse_game_meta_data(self, html: BeautifulSoup) -> dict:
        """
        Provided the BR game page it parses out the game time and
        game arena name.
        :return: dictionary of meta data
        """

        meta_holder = html.select_one("div.scorebox_meta")

        game_time = str_to_datetime(
            meta_holder.find("div").text, ["%I:%M %p, %B %d, %Y", "%B %d, %Y"]
        )

        arena_name = meta_holder.find_all("div")[1].text.split(",")[0]

        return {
            "game_time": game_time,
            "arena_name": arena_name,
        }

    def _parse_game_id(self, game_url: str) -> str:
        """
        Provided a BR game url it parses out the game id.
        :return: game id as a string.
        """

        return (
            parse.urlsplit(game_url).path.split("/")[-1].replace(".html", "")
        )

    def _parse_basic_stats(
        self, page: BeautifulSoup, team: str, team_sn: str
    ) -> dict[str, int | float]:
        """
        Provided the BR game page it parses out the basic stats
        for either the home or the road team, depending on the
        passed parameter.
        :team: inidcates if it team is home or away
        :return: dictionary of basic stats
        """

        table_finder = f"#box-{team_sn.upper()}-game-basic"

        table = page.select_one(table_finder)
        tb_foot = table.select_one("tfoot")

        game_dic = {
            f"{team}_fg": int(tb_foot.select_one("td[data-stat=fg]").text),
            f"{team}_fga": int(tb_foot.select_one("td[data-stat=fga]").text),
            f"{team}_fg_pct": float(
                tb_foot.select_one("td[data-stat=fg_pct]").text
            ),
            f"{team}_fg3": int(tb_foot.select_one("td[data-stat=fg3]").text),
            f"{team}_fg3a": int(tb_foot.select_one("td[data-stat=fg3a]").text),
            f"{team}_fg3_pct": float(
                tb_foot.select_one("td[data-stat=fg3_pct]").text
            ),
            f"{team}_ft": int(tb_foot.select_one("td[data-stat=ft]").text),
            f"{team}_fta": int(tb_foot.select_one("td[data-stat=fta]").text),
            f"{team}_ft_pct": float(
                tb_foot.select_one("td[data-stat=ft_pct]").text
            ),
            f"{team}_orb": int(tb_foot.select_one("td[data-stat=orb]").text),
            f"{team}_drb": int(tb_foot.select_one("td[data-stat=drb]").text),
            f"{team}_trb": int(tb_foot.select_one("td[data-stat=trb]").text),
            f"{team}_ast": int(tb_foot.select_one("td[data-stat=ast]").text),
            f"{team}_stl": int(tb_foot.select_one("td[data-stat=stl]").text),
            f"{team}_blk": int(tb_foot.select_one("td[data-stat=blk]").text),
            f"{team}_tov": int(tb_foot.select_one("td[data-stat=tov]").text),
            f"{team}_pf": int(tb_foot.select_one("td[data-stat=pf]").text),
            f"{team}_pts": int(tb_foot.select_one("td[data-stat=pts]").text),
        }

        return game_dic


def str_to_datetime(date_str: str, formats: list[str]) -> datetime:
    """
    tries to convert a string date into a datetime with multiple formats.
    If none of the formats work a default datetime is returned.
    """

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass

    return datetime(1900, 1, 1)