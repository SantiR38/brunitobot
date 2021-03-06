import logging
import random
from datetime import date
from schedule import every

from audio_video.constants import (ASSIGNED, GREETING, GREETING_QUESTION,
    GOODBYE)
from brunitobot.task_manager import BrunitoTaskManager
from settings import settings


logging.basicConfig(filename='api_errors.log', level=logging.DEBUG)
ZOOM = 'zoom'
NEW_WEEK = 'new_week'


class AudioVideoMessage(BrunitoTaskManager):
    chat_id = settings.AUDIO_VIDEO_GROUP_ID

    def _create_message(self, message_type: str) -> str:
        week = date.today().isocalendar()[1] % 5
        assigned = ASSIGNED[week]
        if message_type == NEW_WEEK:
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
        elif message_type == ZOOM:
            message = (
                f'{assigned["attendant"]}, hoy abre la reunión de Zoom.'
            )
        return message

    def _send_message(self, message_type: int) -> None:
        message = self._create_message(message_type)
        self._perform_sending(message)

    def send_message_new_week(self):
        self._send_message(NEW_WEEK)

    def send_message_zoom(self):
        self._send_message(ZOOM)

    def schedule_tasks(self):
        """
        Schedule an audio video message to be sent to the user.
        """
        hour = self._to_local_hour(17, 0)
        every().monday.at(hour).do(self.send_message_new_week)

        hour2 = self._to_local_hour(18, 30)
        every().thursday.at(hour2).do(self.send_message_zoom)

        hour3 = self._to_local_hour(9, 0)
        every().sunday.at(hour3).do(self.send_message_zoom)
