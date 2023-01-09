## mypackage\baskref_url_scraper.py

from dataclasses import dataclass
from datetime import date
from urllib import parse
from bs4 import BeautifulSoup
from mypackage.html_scraper import HTMLScraper

@dataclass
class BaskRefUrlScraper(HTMLScraper):
    """
    Class used for generating the URLs for scraping BasketballRefernce.
    Besides simple generation it also includes scraping and parsing needed
    to provide final urls.
    """

    base_url: str = "https://www.basketball-reference.com"

    # public functions

    def get_game_urls_day(self, game_date: date) -> list:
        """
        Scrapes the urls to every game's boxscore on a specific day.
        :game_date: A game_date to scrape games on
        :return: a list of basketball reference urls
        """

        return self._scrape_game_urls_day(
            self._generate_daily_games_url(game_date)
        )

    # private functions

    ## scraping functions

    def _scrape_game_urls_day(self, daily_games_url: str) -> list:
        """
        Scrapes the urls to every game's boxscore on a specific day.
        :daily_games_url: Url to the games on that day
        :return: a list of basketball reference urls
        """

        return self.scrape(daily_games_url, self._parse_daily_games)

    ## parsing functions

    def _parse_daily_games(self, daily_games_page: BeautifulSoup) -> list:
        """
        Parses the games out of the html containing daily games.
        :game_date: A game_date to scrape games on
        :return: a list of basketball reference urls
        """

        element_finder = "div.game_summary > p.links"
        game_urls = []

        for p in daily_games_page.select(element_finder):
            anch = p.find("a")
            if anch is not None:
                url = anch.attrs["href"]
                game_urls.append(self.base_url + url)  #

        return game_urls

    # # helper functions

    def _generate_daily_games_url(self, game_date: date) -> str:
        """Generates the url for all games in a given day"""

        if not isinstance(game_date, date):
            raise ValueError("game_date must be a valid date")

        params = parse.urlencode(
            {
                "month": game_date.month,
                "day": game_date.day,
                "year": game_date.year,
            }
        )

        return f"{self.base_url}/boxscores/?{params}"