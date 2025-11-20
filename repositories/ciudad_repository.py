# repositories/ciudad_repository.py
from database.connection import get_connection


def obtener_ciudad_por_nombre(nombre: str):
    """
    Devuelve un dict con la ciudad si existe, o None si no existe.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id_ciudad, nombre, provincia, pais
                FROM ciudad
                WHERE nombre = %s;
                """,
                (nombre,)
            )
            row = cur.fetchone()

        if row:
            return {
                "id_ciudad": row[0],
                "nombre": row[1],
                "provincia": row[2],
                "pais": row[3],
            }
        return None
    finally:
        conn.close()


def crear_ciudad(nombre: str, provincia: str, pais: str):
    """
    Inserta una ciudad nueva y devuelve su id.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ciudad (nombre, provincia, pais)
                VALUES (%s, %s, %s)
                RETURNING id_ciudad;
                """,
                (nombre, provincia, pais)
            )
            new_id = cur.fetchone()[0]
        conn.commit()
        return new_id
    finally:
        conn.close()
