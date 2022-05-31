import logging
import random
import requests
import schedule
import time
from datetime import date, datetime

from constants import (ASSIGNED, GREETING, GREETING_QUESTION, GOODBYE,
    TELEGRAM_BOT_URL, TELEGRAM_GROUP_ID)


logging.basicConfig(filename='api_errors.log', level=logging.DEBUG)


def create_message(message_number: int) -> str:
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


def send_message(message_number: int) -> None:
    message = create_message(message_number)
    url = TELEGRAM_BOT_URL + "sendMessage"
    data = {
        "chat_id": TELEGRAM_GROUP_ID,
        "text": message,
        "parse_mode": "MarkdownV2"
    }
    response = requests.post(url, data)

    if response.status_code != 200:
        logging.error(f"Date {datetime.now()}:\n{response.text}\n")
    print(response.json())


def send_message_1():
    send_message(1)


def send_message_2():
    send_message(2)


if __name__ == '__main__':
    schedule.every().monday.at("17:00").do(send_message_1)
    schedule.every().thursday.at("18:30").do(send_message_2)
    schedule.every().sunday.at("09:00").do(send_message_2)

    while True:
        schedule.run_pending()
        time.sleep(1)
