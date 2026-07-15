import sqlite3
import logging

logger = logging.getLogger(__name__)

def insert_new_config(db: str, free_ip: str, public_key: str, private_key: str, owner_id: int) -> int:
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO configs (owner_id, ip, public_key, private_key, status) VALUES (?, ?, ?, ?, ?); ", (owner_id, free_ip, public_key, private_key, "active"))
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
    
def get_config_by_id(db: str, id: int) -> dict:
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM configs WHERE id = ?", (id,),)
        row = cursor.fetchone()
        return dict(row) if row else None