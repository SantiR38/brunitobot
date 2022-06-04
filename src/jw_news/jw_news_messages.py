import logging
import requests
from datetime import datetime

from .parser import Parser, pprint
from settings import telegram


logging.basicConfig(filename='api_errors.log', level=logging.DEBUG)

class JWNewsClient:
    url = telegram.BRUNITO_BOT_URL + "sendMessage"
    data = {
        "chat_id": telegram.SANTIAGO_CHAT_ID,
        "parse_mode": "MarkdownV2"
    }

    def perform_sending(self, message):
        self.data['text'] = message
        response = requests.post(self.url, self.data)

        if response.status_code != 200:
            logging.error(f"Date {datetime.now()}:\n{response.text}\n")
        pprint(response.json())

    def send_message(self) -> None:
        content = Parser().get_today_articles()
        
        if any(content):
            title = "*Estas son las noticias de hoy:*"
            self.perform_sending(title)
        for article in content:
            self.perform_sending(article['link'])
            