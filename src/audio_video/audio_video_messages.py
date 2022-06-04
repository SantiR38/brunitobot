import logging
import random
import requests
from datetime import date, datetime
from schedule import every

from audio_video.constants import (ASSIGNED, GREETING, GREETING_QUESTION,
    GOODBYE)
from settings import telegram


logging.basicConfig(filename='api_errors.log', level=logging.DEBUG)


class AudioVideoMessage:
    url = telegram.BRUNITO_BOT_URL + "sendMessage"

    def _create_message(self, message_number: int) -> str:
        week = date.today().isocalendar()[1] % 5
        assigned = ASSIGNED[week]
        if message_number == 1:
            greetings = [
                random.choice(GREETING),
                random.choice(GREETING_QUESTION),
                random.choice(GOODBYE)
            ]
            message = (
                f'{greetings[0]}, {greetings[1]}\n\n'
                f'Estamos en la semana {assigned["week"]}, asi que los asignados son:\n'
                f'*Audio:* {assigned["audio"]}\n'
                f'*Video:* {assigned["video"]}\n'
                f'*Acomodador:* {assigned["attendant"]}\n\n'
                f'{greetings[2]}\\!'
            )
        elif message_number == 2:
            message = (
                f'{assigned["attendant"]}, te recuerdo que hay que iniciar la reunión de zoom 35 min antes\\. Gracias\\!'
            )
        return message

    def _send_message(self, message_number: int) -> None:
        message = self._create_message(message_number)
        data = {
            "chat_id": telegram.AUDIO_VIDEO_GROUP_ID,
            "text": message,
            "parse_mode": "MarkdownV2"
        }
        response = requests.post(self.url, data)

        if response.status_code != 200:
            logging.error(f"Date {datetime.now()}:\n{response.text}\n")
        print(response.json())

    def send_message_new_week(self):
        self._send_message(1)

    def send_message_zoom(self):
        self._send_message(2)

    def schedule_tasks(self):
        """
        Schedule an audio video message to be sent to the user.
        """
        every().monday.at("17:00").do(self.send_message_new_week)
        every().thursday.at("18:30").do(self.send_message_zoom)
        every().sunday.at("09:00").do(self.send_message_zoom)
