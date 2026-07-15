import sqlite3

def init_database(db):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    status STRING NOT NULL
); """)
        
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    ip STRING NOT NULL,
    public_key STRING NOT NULL,
    private_key STRING NOT NULL,
    status STRING NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id)
); """)

        conn.commit()