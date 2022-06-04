import peewee

try:
    database = peewee.SqliteDatabase("src/database/database.db")
except Exception as ex:
    print(ex)
