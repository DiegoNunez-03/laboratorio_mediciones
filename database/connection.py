# database/connection.py
import psycopg2
from .config_db import get_db_config, get_search_path


def get_connection():
    """
    Crea y devuelve una conexión nueva a PostgreSQL
    usando los datos del .env y seteando el search_path.
    """
    db_config = get_db_config()
    conn = psycopg2.connect(**db_config)

    # Setear search_path para no escribir lab_mediciones_db.rango, etc.
    search_path = get_search_path()
    with conn.cursor() as cur:
        cur.execute(f"SET search_path TO {search_path};")

    return conn
