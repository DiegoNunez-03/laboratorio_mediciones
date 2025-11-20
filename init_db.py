# scripts/init_db.py
import os
import psycopg2
from database.config_db import get_db_config, get_search_path



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def run_sql_file(cursor, path):
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    cursor.execute(sql)

def main():
    db_config = get_db_config()
    search_path = get_search_path()

    print("Conectando a PostgreSQL con configuración desde .env...")
    conn = psycopg2.connect(**db_config)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        # 1) Crear schema y tablas
        # schema_path = os.path.join(BASE_DIR, "database", "schema.sql")
        schema_path   = os.path.join(BASE_DIR, "database", "schema.sql")
        print(f"Ejecutando {schema_path} ...")
        run_sql_file(cur, schema_path)

        # 2) Cargar catálogos
        catalogo_path = os.path.join(BASE_DIR, "database", "catalogo.sql")
        print(f"Ejecutando {catalogo_path} ...")
        run_sql_file(cur, catalogo_path)

        # 3) Prueba rápida: ver rangos
        cur.execute(f"SET search_path TO {search_path};")
        cur.execute("SELECT id_rango, nombre_rango, temp_min, temp_max FROM rango;")
        rows = cur.fetchall()

        print("\nRangos cargados:")
        for row in rows:
            print(row)

        print("\n✔ Base de datos inicializada correctamente.")

    except Exception as e:
        print("\n❌ Error inicializando la base de datos:")
        print(e)

    finally:
        cur.close()
        conn.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()
