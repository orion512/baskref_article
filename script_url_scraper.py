from datetime import date
from mypackage.baskref_url_scraper import BaskRefUrlScraper

url_scraper = BaskRefUrlScraper()

url_scraper._generate_daily_games_url(date(2005,12,25))
# https://www.basketball-reference.com/boxscores/index.fcgi?month=12&day=25&year=2005

# from the above url we can parse out the URLs to both games player on 2005-12-25

urls = url_scraper.get_game_urls_day(date(2005,12,25))

print(urls)
# [
#  https://www.basketball-reference.com/boxscores/200512250DET.html,
#  https://www.basketball-reference.com/boxscores/200512250MIA.html,
# ]