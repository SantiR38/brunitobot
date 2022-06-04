import json
import requests
from datetime import date

from bs4 import BeautifulSoup

def pprint(data: dict, sort_keys: bool = False) -> None:
    print(json.dumps(data, indent=4, sort_keys=sort_keys))

class Parser:
    jw_site = 'https://www.jw.org'

    def _get_last_articles(self, num_articles: int) -> list:
        # response = requests.get('https://www.jw.org/en/whats-new/')
        # html = BeautifulSoup(response.text, 'html.parser')
        with open("jw_news/news.html", "r") as f:
            html = BeautifulSoup(f, "html.parser")

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
        article_info['link'] = article_info['link'] \
            .replace(".", "\\.") \
            .replace("-", "\\-")

        return article_info

    def get_today_articles(self) -> list:
        """
        Returns a list of dictionaries representing the articles.
        """
        today = date.today().strftime("%Y-%m-%d")
        last_articles = self._get_last_articles(20)
        articles_json = []
        articles_links = []
        for article in last_articles:
            new_article = self._get_article_info(article)
            if new_article['link'] not in articles_links \
                    and new_article['date'] == today:
                articles_json.append(new_article)
                articles_links.append(new_article['link'])
        return articles_json
