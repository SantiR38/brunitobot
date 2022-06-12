import peewee

try:
    database = peewee.SqliteDatabase("database.db")
except Exception as ex:
    print(ex)
