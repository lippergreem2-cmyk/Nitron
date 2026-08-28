import sqlite3

connection = sqlite3.connect("database.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT

)
""")

connection.commit()

print("Database created successfully.")

connection.close()
