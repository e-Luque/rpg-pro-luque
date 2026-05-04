from database.conexion_db import ConexionDB

class RazaDAO(ConexionDB):
    def __init__(self):
        self.lista_razas = []
    def cargarRazas(self):
        self.cursor.execute("""
            SELECT 
    p.id,
    p.nombre AS personaje,
    p.nivel,
    p.exp,
    p.oro,
    p.vida_max,
    p.vida_actual,
    p.mana_max,
    p.mana_actual,
    p.fuerza,
    p.agilidad,
    p.inteligencia,
    r.nombre AS raza,          -- Traemos el nombre de la tabla Razas
    c.nombre AS clase,         -- Traemos el nombre de la tabla Clases_RPG
    p.creado_en
FROM Personajes p
LEFT JOIN Razas r ON p.id_raza = r.id
LEFT JOIN Clases_RPG c ON p.id_clase = c.id;
        """
        character = cursor.fetchone()
        personaje = Personaje(character[0], character[1], character[2], character[3], character[4], character[5], character[6])
        self.lista_personajes.append(personaje)
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