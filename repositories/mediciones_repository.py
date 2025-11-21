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


def obtener_todas_las_mediciones():
    """
    Devuelve todas las mediciones con info de ciudad y rango.
    """
    # from database.connection import get_connection  

    sql = """
        SELECT
            m.id_mediciones,
            m.fecha,
            m.temperatura,
            m.humedad,
            m.sensacion_termica,
            m.presion,
            m.velocidad_viento,
            m.descripcion,
            c.id_ciudad,
            c.nombre AS ciudad,
            c.provincia,
            c.pais,
            r.id_rango,
            r.nombre_rango
        FROM mediciones m
        JOIN ciudad c ON m.id_ciudad = c.id_ciudad
        JOIN rango r ON m.id_rango = r.id_rango
        ORDER BY m.fecha DESC, m.id_mediciones DESC;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

    resultados = []
    for row in rows:
        resultados.append({
            "id_medicion": row[0],
            "fecha": row[1].isoformat() if row[1] is not None else None,
            "temperatura": row[2],
            "humedad": row[3],
            "sensacion_termica": row[4],
            "presion": row[5],
            "velocidad_viento": row[6],
            "descripcion": row[7],
            "ciudad": {
                "id_ciudad": row[8],
                "nombre": row[9],
                "provincia": row[10],
                "pais": row[11],
            },
            "rango": {
                "id_rango": row[12],
                "nombre_rango": row[13],
            }
        })

    return resultados
