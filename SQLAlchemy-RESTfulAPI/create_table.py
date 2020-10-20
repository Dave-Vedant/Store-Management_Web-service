import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"  # INTEGER PRIMARY KEY assign id automaticaly...
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY,name text, price real)"  # INTEGER PRIMARY KEY assign id automaticaly...
cursor.execute(create_table)

connection.commit()
connection.close()


'''
NOTES : 
No need of running this file because of app.py direct data creating features. 
'''