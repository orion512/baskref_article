from datetime import date
from mypackage.baskref_url_scraper import BaskRefUrlScraper
from mypackage.baskref_data_scraper import BaskRefDataScraper

url_scraper = BaskRefUrlScraper()
urls = url_scraper.get_game_urls_day(date(2005,12,25))

data_scraper = BaskRefDataScraper()
game_data = data_scraper.get_games_data(urls)

print(game_data[1])
