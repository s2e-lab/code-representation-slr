import sqlite3
import os



sqliteConnection = sqlite3.connect('../analyses/db_survey_representations.sqlite3')

sql_query = """SELECT name FROM sqlite_master  
  WHERE type='table';"""

cursor = sqliteConnection.cursor()

cursor.execute(sql_query)

print(cursor.fetchall())