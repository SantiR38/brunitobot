import logging
import requests
from datetime import datetime as dt

from jw_news.parser import pprint
from settings import telegram


logging.basicConfig(filename='api_errors.log', level=logging.DEBUG)


class BrunitoTaskManager:
    url = telegram.BRUNITO_BOT_URL + "sendMessage"
    data = {
        "chat_id": telegram.SANTIAGO_CHAT_ID,
        "parse_mode": "MarkdownV2"
    }

    def _format_message(message: str) -> str:
        return message \
            .replace(".", "\\.") \
            .replace("-", "\\-") \
            .replace("!", "\\!") \

    def _perform_sending(self, message) -> requests.Response:
        self.data['text'] = self._format_message(message)
        response = requests.post(self.url, self.data)

        if response.status_code != 200:
            logging.error(f"Date {dt.now()}:\n{response.text}\n")
        pprint(response.json())
        return response
    
    def schedule_tasks():
        raise NotImplementedError()
