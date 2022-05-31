import os

CATRIEL = "Catriel"
JOSE = "José"
PEDRO = "Pedro"
SANTIAGO = "Santiago"

ASSIGNED = [
    {
        "week": 5,
        "audio": PEDRO,
        "video": CATRIEL,
        "attendant": SANTIAGO
    },
    {
        "week": 1,
        "audio": PEDRO,
        "video": SANTIAGO,
        "attendant": CATRIEL
    },
    {
        "week": 2,
        "audio": SANTIAGO,
        "video": CATRIEL,
        "attendant": JOSE
    },
    {
        "week": 3,
        "audio": PEDRO,
        "video": JOSE,
        "attendant": SANTIAGO
    },
    {
        "week": 4,
        "audio": JOSE,
        "video": CATRIEL,
        "attendant": PEDRO
    }
]

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_BOT_URL = F"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"
TELEGRAM_GROUP_ID = -737888396