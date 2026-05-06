
class PersonajeDAO(ConexionDB):
    def __init__(self):
        super().__init__()
        self.lista_personajes = []

    def obtener_por_id(self, id_personaje):
        self.cursor.execute("""
            SELECT
                p.id,
                p.nombre,
                p.nivel,
                p.exp,
                p.oro,
                p.vida_actual,
                r.nombre AS raza,
                c.nombre AS clase
            FROM Personajes p
            LEFT JOIN Razas r ON p.id_raza = r.id
            LEFT JOIN Clases_RPG c ON p.id_clase = c.id
            WHERE p.id = %s
        """, (id_personaje,))
        return self.cursor.fetchone()

    def cargarPersonajes(self):
        self.cursor.execute("""
            SELECT
                p.id,
                p.nombre,
                p.nivel,
                p.exp,
                p.oro,
                p.vida_actual,
                r.nombre AS raza,
                c.nombre AS clase
            FROM Personajes p
            LEFT JOIN Razas r ON p.id_raza = r.id
            LEFT JOIN Clases_RPG c ON p.id_clase = c.id
            ORDER BY p.id
        """)
        self.lista_personajes = self.cursor.fetchall()

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
