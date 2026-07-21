import sqlite3

def init_database(db):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    status STRING NOT NULL,
    configs_limit INTEGER
); """)
        
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    name STRING NOT NULL DEFAULT '',
    ip STRING NOT NULL,
    public_key STRING NOT NULL,
    private_key STRING NOT NULL,
    status STRING NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id)
); """)

        cursor.execute("PRAGMA table_info(users)")
        user_columns = {row[1] for row in cursor.fetchall()}
        if "configs_limit" not in user_columns:
            cursor.execute("ALTER TABLE users ADD COLUMN configs_limit INTEGER")

        cursor.execute("PRAGMA table_info(configs)")
        config_columns = {row[1] for row in cursor.fetchall()}
        if "name" not in config_columns:
            cursor.execute("ALTER TABLE configs ADD COLUMN name STRING NOT NULL DEFAULT ''")

        conn.commit()
