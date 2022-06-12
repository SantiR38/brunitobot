import logging
import peewee


logging.basicConfig(filename='api_errors.log', level=logging.DEBUG)


try:
    database = peewee.SqliteDatabase("database.db")
except Exception as ex:
    logging.error(ex)
