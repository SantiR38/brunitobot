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

GREETING = [
    "Hola muchachos",
    "Hola chicos",
    "Genios",
    "Hola mis queridos",
    "Buenas",
    "Buenas y santas",
    "Estimadisimos",
    "Estimados",
    "Aca molestando de nuevo",
    "Hola",
    "Buenas tardes muchachos",
    "Buenas tardes chicos",
    "Buenas tardes"
]

GREETING_QUESTION = [
    "como estan?",
    "todo tranquilo?",
    "como va?",
    "como va eso?",
    "que talco?",
    "todo bien?",
    "como andan?",
    "que cuentan?",
    "que se cuenta?",
    "como los trata la vida?",
    "que tal ese inicio de semana?"
]

GOODBYE = [
    "Chau gente, se cuidan",
    "Chau gente, cuidense",
    "Chau gente",
    "Chau muchachos, se cuidan",
    "Chau muchachos, cuidense",
    "Chau muchachos",
    "Nos vemos, abrazo",
    "Abrazo",
    "Abrazo cuidense",
    "Nos vemos",
    "Nos vemos, cuidense",
    "Nos vemos, abrazo",
]
