# database/config_db.py
import os
from dotenv import load_dotenv

# Cargar variables desde .env
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

def get_db_config():
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("DB_NAME", "lab_mediciones_db"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "@Gb0206Dn"),
    }

def get_search_path():
    # para usar después en SET search_path ...
    return os.getenv("DB_SEARCH_PATH", "lab_mediciones_db,public")
