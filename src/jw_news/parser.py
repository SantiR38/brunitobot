import json
import logging
import requests
from datetime import date, datetime as dt, timedelta as td
from bs4 import BeautifulSoup

from jw_news.models import JWNews
from settings import settings


logging.basicConfig(filename='api_errors.log', level=logging.DEBUG)


def dprint(data: dict, sort_keys: bool = False) -> None:
    if settings.DEBUG:
        print(json.dumps(data, indent=4, sort_keys=sort_keys))


class Parser:
    jw_site = 'https://www.jw.org'

    def _parse_html(self) -> BeautifulSoup:
        if not settings.DEBUG:
            response = requests.get(f'{self.jw_site}/en/whats-new/')
            return BeautifulSoup(response.text, 'html.parser')
        with open("src/jw_news/news.html", "r") as f:
            return BeautifulSoup(f, "html.parser")

    def _get_last_articles(self, num_articles: int) -> list:
        try:
            html = self._parse_html()
        except Exception as e:
            logging.error(f"Date {dt.now()}:\n{e}")
            return []
        new_articles_section = html.body.article.find(
            "div", class_="whatsNewItems").find_all("div", class_="syn-body")

        last_articles = new_articles_section[:num_articles]
        return last_articles

    def _get_article_info(self, article) -> dict:
        article_info = {}
        article_info['link'] = article.find("a").get("href")
        article_info['date'] = article.find("p", class_="pubDate").text
        
        if article_info['link'].startswith("/en"):
            article_info['link'] = self.jw_site + article_info['link']
        article_info['link'] = article_info['link']

        return article_info

    def get_today_articles(self) -> list:
        """
        Returns a list of dictionaries representing the articles.
        """
        today = date.today().strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
        yesterday = (date.today()-td(days=1)).strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
        last_articles = self._get_last_articles(20)
        articles_json = []
        articles_links = []
        for article in last_articles:
            new_article = self._get_article_info(article)

            repeated_link = new_article['link'] in articles_links
            article_is_old = new_article['date'] not in [today, yesterday]

            if repeated_link or article_is_old:
                continue

            not_already_sended = JWNews.select() \
                .where(JWNews.link == new_article['link']) \
                .count() == 0

            if not_already_sended:
                articles_json.append(new_article)
                articles_links.append(new_article['link'])

        return articles_json
