import re
import requests
import time
import pandas as pd
import time
from news_config import *
from base import *
from bs4 import BeautifulSoup

from urllib import request


def Main(todays_news):

    date_today = time.strftime("%d %b %Y")  # dd mmm yyyy
    print("\tCollecting news for {}.\n".format(date_today))

    articles_fetched = 0

    # news categories (cat)
    print("Fetching {} categories: ".format(len(st_categories)))
    for (cat, cat_url) in st_categories:
        print("\t[{}]".format(cat))

    # urls of articles for each category
    st_cats_urls = []
    for (cat, cat_url) in st_categories:
        urls = articleURLs(articleHTML(cat_url), headline_count)
        st_cats_urls.append((urls, cat))
        articles_fetched += len(urls)

    st_articles = [urls for urls in st_cats_urls]
    news_data = {
        'Category': [],
        'News': [],
        'Date': []
    }
    # look at each news category
    for (urls, cat) in st_articles:

        df_cat = []
        df_content = []
        df_date = []
        print("Parsing Category: {}".format(cat.lower()))
        for url in urls:
            # article data
            html = articleHTML(url)
            js = articleJavaScript(html)
            pub_datetime = articleDateTime(js)
            pub_date = articleDate(pub_datetime)
            pub_time = articleTime(pub_datetime)

            if todays_news is True and pub_date != date_today:
                # skip to next article if it's not published today
                continue
            else:
                cat_in_url = urlCategory(url)
                subcat_in_url = urlSubCategory(url)

                # get news subcategory;
                # otherwise, get main category
                if subcat_in_url is None:
                    subcat_in_url = cat_in_url

                pub_id = "#{}".format(articleID(js))
                title = pub_id+" "+articleTitle(html)
                byline = articleByline(html)
                keywords = articleKeywords(js)
                text = articleText(url)
                try:
                    content = title[len(pub_id):]
                except:
                    content = ''

                n = len(content)

                df_content.append(content)
                df_date.append(pub_date)
            df_cat.append(cat)
        print(len(df_date), len(df_cat), len(df_content))
        news_data['Category'] += df_cat
        news_data['News'] += df_content
        news_data['Date'] += df_date

    newsdf = pd.DataFrame(news_data)
    print("\nArticles fetched: {}\n".format(articles_fetched))
    print(newsdf)


if __name__ == "__main__":
    Main(todays_news)
