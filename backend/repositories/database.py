import MySQLdb
import os

HOST = os.getenv("DATABASE_HOST")
USER = os.getenv("DATABASE_USER")
PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE")

db = MySQLdb.connect(
    host=HOST,
    user=USER,
    passwd=PASSWORD,
    db=DATABASE_NAME,
    autocommit=False,
)

cursor = db.cursor(MySQLdb.cursors.DictCursor)