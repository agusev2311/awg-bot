import os
from dotenv import load_dotenv

def get_config():
    load_dotenv()
    token = os.getenv("AWG_TG_TOKEN")
    admin_id = os.getenv("AWG_TG_ADMIN_ID")
    db_filename = os.getenv("AWG_DB_FILENAME")
    return {
        "token": token,
        "admin_id": admin_id,
        "db_filename": db_filename
    }

