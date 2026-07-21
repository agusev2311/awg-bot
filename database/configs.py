import sqlite3
import logging

logger = logging.getLogger(__name__)

def insert_new_config(db: str, free_ip: str, public_key: str, private_key: str, owner_id: int, name: str) -> int:
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO configs (owner_id, name, ip, public_key, private_key, status) VALUES (?, ?, ?, ?, ?, ?); ",
            (owner_id, name, free_ip, public_key, private_key, "active"),
        )
        id = cursor.lastrowid
        logger.info(f"config with id %s created", id)
        conn.commit()
        return id
    
def get_all_configs(db: str) -> dict:
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM configs")
        return [dict(row) for row in cursor.fetchall()]

def get_all_used_ips(db: str) -> set[str]:
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ip FROM configs")
        return {row[0] for row in cursor.fetchall() if row[0]}
    
def get_config_by_id(db: str, id: int) -> dict:
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM configs WHERE id = ?", (id,),)
        row = cursor.fetchone()
        return dict(row) if row else None

def get_user_configs_page(db: str, owner_id: int, page: int, per_page: int) -> tuple[list[dict], int]:
    offset = max(page - 1, 0) * per_page
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM configs WHERE owner_id = ? AND status != ?", (owner_id, "deleted"))
        total_configs = cursor.fetchone()[0]
        cursor.execute(
            "SELECT * FROM configs WHERE owner_id = ? AND status != ? ORDER BY id DESC LIMIT ? OFFSET ?",
            (owner_id, "deleted", per_page, offset),
        )
        rows = cursor.fetchall()
    return [dict(row) for row in rows], total_configs

def count_user_configs(db: str, owner_id: int) -> int:
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM configs WHERE owner_id = ? AND status != ?", (owner_id, "deleted"))
        return cursor.fetchone()[0]

def get_user_config_by_id(db: str, owner_id: int, config_id: int) -> dict | None:
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM configs WHERE id = ? AND owner_id = ? LIMIT 1", (config_id, owner_id))
        row = cursor.fetchone()
    return dict(row) if row else None

def update_config_name(db: str, config_id: int, name: str):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE configs SET name = ? WHERE id = ?", (name, config_id))
        conn.commit()

def update_config_status(db: str, config_id: int, status: str):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE configs SET status = ? WHERE id = ?", (status, config_id))
        conn.commit()

def delete_config(db: str, config_id: int):
    update_config_status(db, config_id, "deleted")

def get_configs_page(db: str, page: int, per_page: int) -> tuple[list[dict], int]:
    offset = max(page - 1, 0) * per_page
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM configs WHERE status != ?", ("deleted",))
        total_configs = cursor.fetchone()[0]
        cursor.execute(
            "SELECT * FROM configs WHERE status != ? ORDER BY id DESC LIMIT ? OFFSET ?",
            ("deleted", per_page, offset),
        )
        rows = cursor.fetchall()
    return [dict(row) for row in rows], total_configs
