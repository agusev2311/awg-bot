import sqlite3
import logging

logger = logging.getLogger(__name__)

def create_user(db, id: int):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (id) VALUES (?); ", (id,))
        conn.commit()
    logger.info(f"user with id %s created", id)

def user_exists(db, id: int):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ? LIMIT 1", (id,))
        result = cursor.fetchone()
    return result is not None

def create_user_if_not_exist(db, id: int):
    if not user_exists(db, id):
        create_user(db, id)