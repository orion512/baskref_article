## mypackage\__init__.py

import argparse
from datetime import date, datetime
from mypackage.baskref_url_scraper import BaskRefUrlScraper
from mypackage.baskref_data_scraper import BaskRefDataScraper

def run_mypackage() -> None:
    """Entry point script which runs mypackage"""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d",
        "--date",
        help="""
        This parameter specifies the date
        when the games were played. 
        By default it will be set to today.
        """,
        default=date.today().strftime("%Y-%m-%d"),
        type=valid_date,
    )

    parameters = parser.parse_args()

    url_scraper = BaskRefUrlScraper()
    urls = url_scraper.get_game_urls_day(parameters.date)
    
    data_scraper = BaskRefDataScraper()
    game_data = data_scraper.get_games_data(urls)

    # for the purpose of thsi article we print the scraped data
    # in reality you might want to return it or save it into a CSV
    print(game_data)

def valid_date(str_date: str) -> date:
    """Validates if the passed string is a valid date"""
    try:
        return datetime.strptime(str_date, "%Y-%m-%d").date()
    except (ValueError, TypeError) as exc:
        raise ValueError(f"not a valid date: {str_date!r}") from exc