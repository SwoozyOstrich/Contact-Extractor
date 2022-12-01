from Scrapy import my_spider
import pandas as pd
from time import sleep

bad_words = ['instagram', 'youtube', 'twitter', 'wiki', 'doordash', 'sentry', 'toasttab', 'yelp', 'restaurantji']

#my_spider.get_info('AMERICAN BULL BAR & GRILL THE', 2, 'pt', 'test.csv', reject=bad_words)

burlingame_accounts = pd.read_csv('data/burlingame_accounts.csv')
burlingame_accounts = burlingame_accounts['searchterm'].tolist()

for account in burlingame_accounts:
    my_spider.get_info(account, 2, 'pt', 'burlingame_emails.csv', reject=bad_words)
    sleep(5)

