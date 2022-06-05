import logging
import random
from datetime import date
from schedule import every

from audio_video.constants import (ASSIGNED, GREETING, GREETING_QUESTION,
    GOODBYE)
from brunitobot.task_manager import BrunitoTaskManager
from settings import settings


logging.basicConfig(filename='api_errors.log', level=logging.DEBUG)


class AudioVideoMessage(BrunitoTaskManager):
    data = {
        "chat_id": settings.AUDIO_VIDEO_GROUP_ID,
        "text": "",
        "parse_mode": "MarkdownV2"
    }
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
                f'{greetings[2]}!'
            )
        elif message_number == 2:
            message = (
                f'{assigned["attendant"]}, hoy abre la reunión de Zoom.'
            )
        return message

    def _send_message(self, message_number: int) -> None:
        message = self._create_message(message_number)
        self._perform_sending(message)

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
