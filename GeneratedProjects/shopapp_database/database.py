
import sqlite3


def connect():

    db = sqlite3.connect(
        "app.db"
    )

    return db



def create_users():

    db = connect()

    cursor = db.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
        '''
    )

    db.commit()

    db.close()


create_users()
