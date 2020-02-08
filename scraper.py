import bs4 as bs
import urllib.request
import pandas as pd
from datetime import datetime
import re
from sql import *

source = urllib.request.urlopen('https://www.sgvtribune.com/').read()

soup = bs.BeautifulSoup(source, 'lxml')

database = r"db/sgvheadlines.db"

def insert_trending_headlines():
    dateformat = '%a %B %d, %Y'
    date = datetime.now().strftime(dateformat)
    span = soup.find_all('span', class_='dfm-title')
    for headlines in span[5:17]:
        article_name = re.sub('[\n+\t+]', '', headlines.text)
        # data = pd.DataFrame(dict(Headlines=[re.sub('[\n+\t+]', '', headlines.text)], Date=[date]))
        insert_headline(article_name, date)

if __name__ == "__main__":
    insert_trending_headlines()