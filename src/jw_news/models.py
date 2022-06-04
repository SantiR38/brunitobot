import peewee
from datetime import datetime as dt

from db_connection import database

class JWNews(peewee.Model):
    link = peewee.CharField(max_length=350, unique=True, index=True)
    date_release = peewee.CharField(max_length=10)
    date_created = peewee.DateField(default=dt.now)

    class Meta:
        database = database
        da_table = "JWNews"