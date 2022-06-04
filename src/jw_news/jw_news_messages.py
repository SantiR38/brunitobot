import logging
import requests
from datetime import datetime as dt, timedelta as td
from schedule import every

from jw_news.parser import Parser, pprint
from jw_news.models import JWNews
from settings import telegram


logging.basicConfig(filename='api_errors.log', level=logging.DEBUG)


class JWNewsClient:
    url = telegram.BRUNITO_BOT_URL + "sendMessage"
    data = {
        "chat_id": telegram.SANTIAGO_CHAT_ID,
        "parse_mode": "MarkdownV2"
    }

    def _perform_sending(self, message) -> requests.Response:
        self.data['text'] = message
        response = requests.post(self.url, self.data)

        if response.status_code != 200:
            logging.error(f"Date {dt.now()}:\n{response.text}\n")
        pprint(response.json())
        return response

    def send_message(self) -> None:
        content = Parser().get_today_articles()
        
        if any(content):
            title = "*Estas son las noticias de hoy:*"
            self._perform_sending(title)
        for article in content:
            response = self._perform_sending(article['link'])
            if response.status_code != 200:
                continue
            JWNews.create(
                link=article['link'],
                date_release=article['date']
            )

    def delete_old_links(self):
        three_days_ago = dt.now() - td(days=3)
        old_articles = JWNews.delete().where(
            JWNews.date_release < three_days_ago
        )
        deletions = old_articles.execute()
        
        logging.info(f"Date {dt.now()}:\n{deletions} articles deleted")

    def schedule_tasks(self) -> None:
        """
        Schedule messages sendings and db instances deletions.
        """
        every().day.at("10:00").do(self.send_message)
        every().day.at("19:30").do(self.send_message)

        every().sunday.at("03:00").do(self.delete_old_links)