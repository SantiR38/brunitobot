import logging
import requests
from datetime import datetime as dt, timedelta as td

from jw_news.parser import pprint
from settings import settings


logging.basicConfig(filename='api_errors.log', level=logging.DEBUG)


class BrunitoTaskManager:
    url = settings.BRUNITO_BOT_URL + "sendMessage"
    data = {
        "chat_id": settings.SANTIAGO_CHAT_ID,
        "parse_mode": "MarkdownV2"
    }

    def _format_message(self, message: str) -> str:
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

    def _to_local_hour(self, hour: int, minute: int) -> str:
        """
        Return local hour with format `HH:MM`
        """
        dtime = dt(2022, 6, 5, hour, minute)
        local_time = dtime + td(hours=settings.DIFF_HOURS)
        return local_time.strftime("%H:%M")

    def schedule_tasks(self) -> None:
        """
        Schedules tasks
        ---
        This method will be called by the main script.

        IMPORTANT: Allways use method `_to_local_hour()` to generate the hour
        of the schedule.
        """
        raise NotImplementedError()
