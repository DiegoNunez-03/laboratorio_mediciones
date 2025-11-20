# repositories/mediciones_repository.py
from database.connection import get_connection


def obtener_rango_por_temperatura(temperatura: int):
    """
    Devuelve el id_rango correspondiente a la temperatura dada,
    según los campos temp_min y temp_max de la tabla rango.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id_rango, nombre_rango
                FROM rango
                WHERE (temp_min IS NULL OR %s >= temp_min)
                  AND (temp_max IS NULL OR %s < temp_max);
                """,
                (temperatura, temperatura)
            )
            row = cur.fetchone()

        if not row:
            return None

        return {
            "id_rango": row[0],
            "nombre_rango": row[1],
        }
    finally:
        conn.close()


def insertar_medicion(
    id_ciudad: int,
    id_rango: int,
    temperatura: int,
    humedad: str,
    sensacion_termica: str,
    presion: str,
    velocidad_viento: str,
    descripcion: str,
):
    """
    Inserta una medición y devuelve el id_mediciones generado.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO mediciones (
                    id_ciudad, id_rango, fecha, temperatura,
                    humedad, sensacion_termica, presion,
                    velocidad_viento, descripcion
                )
                VALUES (
                    %s, %s, CURRENT_DATE, %s,
                    %s, %s, %s,
                    %s, %s
                )
                RETURNING id_mediciones;
                """,
                (
                    id_ciudad,
                    id_rango,
                    temperatura,
                    humedad,
                    sensacion_termica,
                    presion,
                    velocidad_viento,
                    descripcion,
                )
            )
            new_id = cur.fetchone()[0]
        conn.commit()
        return new_id
    finally:
        conn.close()
