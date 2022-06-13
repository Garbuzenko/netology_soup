import requests
import bs4
from fake_headers import Headers

def parse(base_url, keyword):
    header = Headers(browser="chrome", os="win", headers=True)
    responce = requests.get(base_url + '/ru/all/', headers=header.generate())

    articles = bs4.BeautifulSoup(responce.text, features='html.parser').findAll("article")

    for article in articles:
        href = article.find(class_="tm-article-snippet__title tm-article-snippet__title_h2").find("a").attrs["href"]

        responce = requests.get(base_url + href, headers=header.generate())
        article_full = bs4.BeautifulSoup(responce.text, features='html.parser').find(class_="tm-article-presenter__body")

        if any(word in article_full.text for word in keyword):
            date = article.find(class_="tm-article-snippet__datetime-published").find("time").attrs["datetime"][0:10]
            title = article.find(class_="tm-article-snippet__title tm-article-snippet__title_h2").find("span").text
            print(f'{date} - {title} - {base_url + href}')


if __name__ == '__main__':
    base_url = 'https://habr.com'
    KEYWORDS = ['python', 'Kubernetes', 'дизайн']
    parse(base_url, KEYWORDS)
