#!/c/Users/Qi/AppData/Local/Programs/Python/Python37/python

import time
import datetime
import requests
from bs4 import BeautifulSoup
from senti import calc


def get_keywords(soup):
    kws = soup.find("meta", {"name": "keywords"})['content'].split(",")
    kws_separated = ", ".join(kws)
    keywords = f"Keywords: {kws_separated}"
    return keywords


def get_text(soup):
    try:
        article_body = soup.find("div", {"class": "StandardArticleBody_body"})
        paragraphs = article_body.find_all("p")
        paragraph_texts = ''.join([p.get_text() for p in paragraphs])
    except:
        paragraphs = ""
    return paragraph_texts


def get_datetime(headline):
    ms = int(headline['dateMillis'])
    dt = str(datetime.datetime.utcfromtimestamp(ms/1000.0))
    return dt


def get_article(headline):
    url = "http://www.reuters.com" + headline['url']
    article_raw = requests.get(url)
    soup = BeautifulSoup(article_raw.content, "lxml")

    article = {
        'id': headline['id'],
        'text': get_text(soup),
        'headline': headline['headline'],
        'keywords': get_keywords(soup),
        'datetime': get_datetime(headline),
        'url': url
    }
    return article


if __name__ == "__main__":
    t = time.time()
    url = "http://www.reuters.com/assets/jsonWireNews"
    wire_raw = requests.get(url)
    headlines = wire_raw.json()['headlines']
    for i in range(len(headlines)):
        out = get_article(headlines[i])
        sen, tokens, lex = calc(out['text'].upper())
        print('Sentiment:', sen, '|', out['headline'], )
    print(time.time() - t, 'seconds taken')
