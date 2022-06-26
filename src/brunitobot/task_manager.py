import logging
import requests
from datetime import datetime as dt, timedelta as td

from jw_news.parser import dprint
from settings import settings


logging.basicConfig(filename='api_errors.log', level=logging.DEBUG)


class BrunitoTaskManager:
    url = settings.BRUNITO_BOT_URL + "sendMessage"
    chat_id = settings.SANTIAGO_CHAT_ID
    _data = None

    @property
    def data(self):
        if self._data is None:
            self._data = {
                "chat_id": self.chat_id,
                "text": "",
                "parse_mode": "MarkdownV2"
            }
        return self._data

    def _format_message(self, message: str) -> str:
        return message \
            .replace(".", "\.") \
            .replace("-", "\-") \
            .replace("_", "\_") \
            .replace("!", "\!") \
            .replace("#", "\#") \

    def _perform_sending(self, message) -> requests.Response:
        self.data['text'] = self._format_message(message)
        response = requests.post(self.url, self.data)

        if response.status_code != 200:
            logging.error(f"Date {dt.now()}:\n{response.text}\n")
        dprint(response.json())
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
