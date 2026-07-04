import sqlite3

def init_database(db):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY
); """)

        conn.commit()