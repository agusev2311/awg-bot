import os
from dotenv import load_dotenv

def get_config():
    load_dotenv()
    token = os.getenv("AWG_TG_TOKEN")
    admin_id = os.getenv("AWG_TG_ADMIN_ID")
    db_filename = os.getenv("AWG_DB_FILENAME")
    awg_dir = os.getenv("AWG_DIR")
    awg_subnet = os.getenv("AWG_SUBNET")
    awg_subnet_v6 = os.getenv("AWG_SUBNET_V6")
    awg_endpoint = os.getenv("AWG_ENDPOINT")
    awg_public = os.getenv("AWG_SERVER_PUBLIC")
    return {
        "token": token,
        "admin_id": admin_id,
        "db_filename": db_filename,
        "awg_dir": awg_dir,
        "awg_subnet": awg_subnet,
        "awg_subnet_v6": awg_subnet_v6,
        "awg_endpoint": awg_endpoint,
        "awg_public": awg_public
    }

