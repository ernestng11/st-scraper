import re
import requests
import time
import pandas as pd

from news_config import *

from bs4 import BeautifulSoup

from urllib import request


def articleHTML(url):
    '''
    get html soup

    '''

    html = request.urlopen(url).read().decode("utf8")
    soup = BeautifulSoup(html, "html.parser")
    return(soup)


def articleURLs(soup, url_count):
    '''
    Returns article urls of a certain news category

    '''
    st = "http://www.straitstimes.com"
    hrefs = str(soup.find_all(
        "span", class_="story-headline", limit=url_count))
    urls = re.findall('href=\"(.*?)\"', hrefs)
    urls = [st+url for url in urls if urls and "javascript" not in url]
    urls = [url for url in urls if "multimedia/" not in url]
    return(urls)


def urlCategory(url):
    '''
    get category from url

    '''
    pattern = "straitstimes.com/(\w*)/"
    cat = re.search(pattern, url)
    if cat:
        cat = cat.group(1).title()
        return(cat)
    else:
        return(None)


def urlSubCategory(url):
    '''
    get subcategory from url

    '''
    pattern = "straitstimes.com/\w*/([a-z-].*)/"
    subcat = re.search(pattern, url)
    if subcat:
        subcat = subcat.group(1).title()
        if subcat == "Australianz":
            subcat = "Australia-NZ"
        elif subcat == "Se-Asia":
            subcat = "SE-Asia"
        return(subcat)
    else:
        return(None)


def articleTitle(soup):
    '''
    get news title

    '''
    title = soup.find("h1", class_="headline node-title")
    title = title.string
    return(title)


def articleByline(soup):
    '''
    Returns news byline/author. Returns '--' if none is found.


    '''
    author = soup.find("div", class_="author-field author-name")
    designation = soup.find("div", class_="author-designation author-field")

    if author and designation:
        author = str(author.string)
        designation = str(designation.string)
        return(author+" | "+designation)
    elif author:
        author = str(author.string)
        return(author)
    else:
        return("--")


def articleText(url):
    '''
    return news text

    '''
    html = requests.get(url).text
    # text = fulltext(html)
    return(html)


def articleJavaScript(soup):
    '''
    get html script tag
    '''
    script = str(soup.find_all("script"))
    return(script)


def articleID(js):
    """ 
    get article id

    """
    target = '"articleid".*"(\d*)"'
    pub_id = re.search(target, js)
    if pub_id:
        return(pub_id.group(1))


def articleDateTime(js):
    '''
    get datetime of article

    '''
    target = '"pubdate":"(.*)"'
    pubdate = re.search(target, js)
    if pubdate:
        return(pubdate.group(1).split(" "))


def articleDate(pub_datetime):
    '''
    Returns article's published datetime

    '''
    pubdate = pub_datetime[0]
    date = pubdate.split("-")

    year, month, day = date[0], date[1], date[2]

    months = {
        "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
        "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
        "09": "Oct", "10": "Sep", "11": "Nov", "12": "Dec"}

    month_name = months.get(month)
    pub_date = "{} {} {}".format(day, month_name, year)
    return(pub_date)


def articleTime(pub_datetime):
    """Returns article's published time.
    """
    pubtime = pub_datetime[1]
    pub_time = pubtime + " Hours"
    return(pub_time)


def articleKeywords(js):
    '''
    Returns a list of news topics/tags

    '''
    target = '"keyword".*"(.*)"'
    keyword = re.search(target, js)
    if keyword:
        keywords = keyword.group(1).split(",")
    return(keywords)


def sentCount(text):
    '''
    Returns sentence count

    '''
    count = len(sent_tokenize(text))
    return(count)
