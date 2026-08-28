import os


class DatabaseGenerator:

    def __init__(self):
        self.output = "GeneratedProjects"
        os.makedirs(self.output, exist_ok=True)


    def create_sqlite(self, name):

        project = os.path.join(
            self.output,
            name
        )

        os.makedirs(project, exist_ok=True)


        files = {

"database.py":
"""
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
""",


"README.md":
"""
# Nitron Generated Database

Database:
SQLite

Created automatically by Nitron AI.
"""
        }


        for filename, content in files.items():

            with open(
                os.path.join(project, filename),
                "w"
            ) as file:

                file.write(content)


        return f"Database created: {project}"
