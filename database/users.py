import sqlite3
import logging
import config

logger = logging.getLogger(__name__)

def create_user(db, id: int):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (id, status, configs_limit) VALUES (?, ?, ?); ", (id, "not_approved", None))
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
    if int(config.get_config()["admin_id"]) == id:
        approve_user(db, id)

def approve_user(db, id): set_status(db, id, "ok")

def set_status(db, id: int, status):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET status = ? WHERE id = ?", (status, id))
        conn.commit()

def get_status(db: str, id: int) -> str | None:
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM users WHERE id = ? LIMIT 1", (id,))
        result = cursor.fetchone()
    return result[0] if result else None

def is_approved(db: str, id: int):
    return get_status(db, id) == "ok"

def get_users_page(db: str, page: int, per_page: int) -> tuple[list[dict], int]:
    offset = max(page - 1, 0) * per_page
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        cursor.execute(
            """
            SELECT users.id, users.status, COUNT(configs.id) AS configs_count
            FROM users
            LEFT JOIN configs ON configs.owner_id = users.id AND configs.status != 'deleted'
            GROUP BY users.id, users.status
            ORDER BY users.id ASC
            LIMIT ? OFFSET ?
            """,
            (per_page, offset),
        )
        rows = cursor.fetchall()
    return [dict(row) for row in rows], total_users

def get_user_by_id(db: str, id: int) -> dict | None:
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT users.id, users.status, users.configs_limit, COUNT(configs.id) AS configs_count
            FROM users
            LEFT JOIN configs ON configs.owner_id = users.id AND configs.status != 'deleted'
            WHERE users.id = ?
            GROUP BY users.id, users.status, users.configs_limit
            LIMIT 1
            """,
            (id,),
        )
        row = cursor.fetchone()
    return dict(row) if row else None

def set_configs_limit(db: str, id: int, limit: int | None):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET configs_limit = ? WHERE id = ?", (limit, id))
        conn.commit()

def get_effective_configs_limit(db: str, id: int) -> int:
    user = get_user_by_id(db, id)
    if user and user["configs_limit"] is not None:
        return int(user["configs_limit"])
    return int(config.get_config()["max_configs_per_user"])
