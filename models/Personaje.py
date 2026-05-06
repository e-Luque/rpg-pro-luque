
from database.conexion_db import ConexionDB

class Personaje:
    def __init__(self, db_data, raza_obj, clase_obj):
        self.id = db_data[0]
        self.nombre = db_data[1]
        self.nivel = db_data[2]
        self.vida = db_data[5]
        self.raza = raza_obj
        self.clase = clase_obj

    def calcular_ataque_base(self):
        factor = getattr(self.clase, 'multiplicador_daño', 1.0)
        if hasattr(self.clase, 'multiplicador_magico'):
            factor = self.clase.multiplicador_magico

        return self.nivel * factor + self.raza.fuerza

    @staticmethod
    def obtener_personajes(get_db_connection):
        """
        Recibe la función de conexión como parámetro para evitar errores de importación.
        """
        personajes_data = []

        # 1. Usamos tu context manager profesional
        with get_db_connection() as conexion:
            if conexion is None:
                return []

            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT id, nombre, nivel, exp, oro, vida_actual, id_raza, id_clase FROM personajes")
                    filas = cursor.fetchall()

                    for fila in filas:
                        # Desempaquetado rápido de Python (más limpio)
                        id_db, nombre, nivel, exp, oro, vida, raza, clase = fila

                        # Creamos el objeto
                        p = Personaje(id_db, nombre, nivel, exp, oro, vida, raza, clase)

                        # Lo convertimos a diccionario (puedes usar p.__dict__ si quieres ahorrar líneas)
                        personajes_data.append({
                            "id": p.id,
                            "nombre": p.nombre,
                            "nivel": p.nivel,
                            "exp": p.exp,
                            "oro": p.oro,
                            "vida_actual": p.vida_actual,
                            "id_raza": p.id_raza,
                            "id_clase": p.id_clase
                        })

                    print(f"✅ Datos recuperados: {len(personajes_data)} personajes.")
            except Exception as e:
                print(f"❌ Error al consultar personajes: {e}")

        return personajes_data