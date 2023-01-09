## mypackage\html_scraper.py

from dataclasses import dataclass
from typing import Callable, Any
import requests
from requests import Response
from bs4 import BeautifulSoup

@dataclass
class HTMLScraper:
    """Class for scraping the web"""

    proxy: str | None = None

    def scrape(self, url: str, parser_fun: Callable) -> Any:
        """
        This function lays out the skeleton for scraping.
        First sends a GET request to the provided url and then uses
        the provided function to parse out the wanted data.
        """

        page = self.get_page(url)

        soup = BeautifulSoup(page.text, "html.parser")
        return parser_fun(soup)

    def get_page(self, url: str) -> Response:
        """
        This function uses as GET request with a few optional parameters
        to scrape a static webpage from the web.
        """

        with requests.Session() as session:
            page = session.get(url, proxies=self._proxies())

        return page

    def _proxies(self) -> dict | None:
        """If a proxy is passed"""
        if self.proxy:
            return {
                "https": self.proxy,
                "http": self.proxy,
            }
        return None