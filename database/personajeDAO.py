from database.conexion_db import ConexionDB


# Asumo que tienes una clase Personaje definida en otro archivo
from modelos.personaje import Personaje

class PersonajeDAO(ConexionDB):
    def __init__(self):
        # ¡Súper importante! Llamamos al constructor del padre para activar la conexión
        super().__init__()
        self.lista_personajes = []

    def cargarPersonajes(self):
        self.cursor.execute("""
                            SELECT 
    p.id,
    p.nombre,
    p.nivel,
    p.vida_max AS vida,
    r.nombre AS raza,
    c.nombre AS clase
FROM Personajes p
LEFT JOIN Razas r ON p.id_raza = r.id
LEFT JOIN Clases_RPG c ON p.id_clase = c.id;
                            """)
        self.lista_personajes = []

        for row in self.cursor.fetchall():
            nuevo_p = Personaje(
                id=row[0],
                nombre=row[1],
                nivel=row[2],
                vida_max=row[3],
                raza=row[4],
                clase=row[5],
            )
            self.lista_personajes.append(nuevo_p)

        return self.lista_personajes

    def actualizar_oro(self, id_personaje, nuevo_oro):
        """Actualiza el oro de un personaje."""
        self.cursor.execute("""
            UPDATE Personajes SET oro = %s WHERE id = %s
        """, (nuevo_oro, id_personaje))
        self.conn.commit()

    def actualizar_vida(self, id_personaje, nueva_vida):
        """Actualiza la vida actual de un personaje."""
        self.cursor.execute("""
            UPDATE Personajes SET vida_actual = %s WHERE id = %s
        """, (nueva_vida, id_personaje))
        self.conn.commit()