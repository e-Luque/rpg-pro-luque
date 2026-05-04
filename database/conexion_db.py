import psycopg2
from psycopg2 import extras


class ConexionDB:  # En Python usamos PascalCase para clases, como en Java
    def __init__(self):
        self.config = {
            "host": "rpg_game",
            "database": "rpg_game",
            "user": "admin",
            "password": "password123",
            "port": 5432
        }
        self.connection = None  # El equivalente a declarar un campo 'private Connection conn;'

    def conectar(self):
        try:
            # Guardamos la conexión en 'self' para que sea global a la clase
            self.connection = psycopg2.connect(**self.config)
            print("Conectado con éxito al servidor")
        except psycopg2.Error as e:
            print(f"Error tipo SQLException: {e}")

    def ejecutar(self, consulta, parametros=None):
        # 1. Usamos el 'self.connection' que creamos en conectar()
        # 2. El 'with' funciona como el "Try-with-resources" de Java 7+
        #    Cierra el cursor automáticamente al terminar.
        with self.connection.cursor(cursor_factory=extras.DictCursor) as cursor:
            cursor.execute(consulta, parametros)

            # Si la consulta es un SELECT, devolvemos los datos
            if cursor.description:
                return cursor.fetchall()

            # Si es un INSERT/UPDATE, hacemos el commit (como en JDBC)
            self.connection.commit()