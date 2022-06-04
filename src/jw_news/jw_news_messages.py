import logging
from datetime import datetime as dt, timedelta as td
from schedule import every

from brunitobot.task_manager import BrunitoTaskManager
from jw_news.parser import Parser
from jw_news.models import JWNews


logging.basicConfig(filename='api_errors.log', level=logging.DEBUG)


class JWNewsClient(BrunitoTaskManager):
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