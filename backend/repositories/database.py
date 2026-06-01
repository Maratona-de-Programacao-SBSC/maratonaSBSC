import mysql.connector
import os


HOST = os.getenv("DATABASE_HOST")
USER = os.getenv("DATABASE_USER")
PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE")

db = mysql.connector.connect(
    host=HOST,
    user=USER,
    passwd=PASSWORD,
    database=DATABASE_NAME,
    autocommit=False,
    allow_local_infile=True
)

cursor = db.cursor(dictionary=True)
