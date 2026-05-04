import os

import psycopg2


class ConexionDB:  # En Python usamos PascalCase para clases, como en Java
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        self.config = {
            "host": os.getenv("POSTGRES_HOST", "localhost"),
            "database": os.getenv("POSTGRES_DB", "rpg_db"),
            "user": os.getenv("POSTGRES_USER", "rpguser"),
            "password": os.getenv("POSTGRES_PASSWORD", "rpgpassword"),
            "port": int(os.getenv("POSTGRES_PORT", "5432")),
        }
        self.connection = None
        self.conn = None
        self.cursor = None
        self.conectar()

    def conectar(self):
        try:
            if self.database_url:
                self.connection = psycopg2.connect(self.database_url)
            else:
                self.connection = psycopg2.connect(**self.config)

            self.conn = self.connection
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            print(f"Error tipo SQLException: {e}")
            raise

    def ejecutar(self, consulta, parametros=None):
        with self.connection.cursor() as cursor:
            cursor.execute(consulta, parametros)

            if cursor.description:
                return cursor.fetchall()

            self.connection.commit()

    def cerrar(self):
        if self.cursor and not self.cursor.closed:
            self.cursor.close()
        if self.connection and not self.connection.closed:
            self.connection.close()
