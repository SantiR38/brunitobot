from asyncio.log import logger
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


class JWAPI:
    def __init__(self):
        """
        Dates are in the format of YYYY-MM-DD
        """
        self.today = date.today().strftime("%Y-%m-%d")
        self.yesterday = (date.today()-td(days=1)).strftime("%Y-%m-%d")
        self.links = []

    def _filter_content(self, content) -> bool:
        article_is_old = content['date'] not in [self.today, self.yesterday]
        is_repeated = content['link'] in self.links

        if is_repeated or article_is_old:
            return False

        not_already_sended = JWNews.select() \
            .where(JWNews.link == content['link']) \
            .count() == 0

        if not_already_sended:
            self.links.append(content['link'])
        return not_already_sended


class JWVideosAPI(JWAPI):
    api_url = ('https://b.jw-cdn.org/apis/mediator/v1/'
        'categories/E/LatestVideos?detailed=1&clientType=www')
    videos_url = 'https://www.jw.org/en/library/videos/#en/mediaitems/LatestVideos/'

    def _map_videos(self, video):
        mapped_video = {
            'link': self.videos_url + video['naturalKey'],
            'date': video['firstPublished'][:10]
        }
        return mapped_video

    def get_latest_videos(self):
        response = requests.get(self.api_url)
        if response.status_code != 200:
            logger.error(f"Date {dt.now()}: {response.content}")
            return []
        media = response.json()['category']['media']
        videos = map(self._map_videos, media)
        videos = list(filter(self._filter_content, videos))
        return videos


class Parser(JWAPI):
    jw_site = 'https://www.jw.org'

    def _parse_html(self) -> BeautifulSoup:
        if not settings.DEBUG:
            response = requests.get(f'{self.jw_site}/en/whats-new/')
            return BeautifulSoup(response.text, 'html.parser')
        with open("src/jw_news/news.html", "r") as f:
            return BeautifulSoup(f, "html.parser")

    def _get_article_info(self, article) -> dict:
        article_info = {}
        article_info['link'] = article.find("a").get("href")
        article_info['date'] = article.find("p", class_="pubDate").text
        
        if article_info['link'].startswith("/en"):
            article_info['link'] = self.jw_site + article_info['link']
        article_info['link'] = article_info['link']

        return article_info

    def _get_lastest_articles(self, num_articles: int=20) -> list:
        try:
            html = self._parse_html()
        except Exception as e:
            logging.error(f"Date {dt.now()}:\n{e}")
            return []
        new_articles_section = html.body.article.find(
            "div", class_="whatsNewItems").find_all("div", class_="syn-body")

        last_articles: list[BeautifulSoup] = new_articles_section[:num_articles]
        articles = map(self._get_article_info, last_articles)
        articles = filter(self._filter_content, articles)
        return list(articles)

    def get_today_articles(self) -> list:
        """
        Returns a list of dictionaries representing the articles.
        """
        lastest_articles = self._get_lastest_articles()
        latest_videos = JWVideosAPI().get_latest_videos()

        return lastest_articles + latest_videos
