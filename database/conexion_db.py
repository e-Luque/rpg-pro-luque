import os
from contextlib import contextmanager

import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://rpguser:rpgpassword@db:5432/rpg_db")


class ConexionDB:
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cursor = self.conn.cursor()

    def cerrar(self):
        self.cursor.close()
        self.conn.close()


@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        yield conn
    except Exception as e:
        print(f"Error al conectar: {e}")
        print(f"DEBUG: Intentando conectar a -> {DATABASE_URL}")
        raise
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    try:
        with get_db_connection():
            print("Conexion exitosa a la base de datos")
    except Exception as e:
        print(f"Error de conexion: {e}")
