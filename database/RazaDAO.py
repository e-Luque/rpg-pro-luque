from database.conexion_db import ConexionDB

class RazaDAO(ConexionDB):
    def __init__(self):
        super().__init__()
        self.lista_razas = []

    def cargarRazas(self):
        self.cursor.execute("""
            SELECT
                id,
                nombre,
                descripcion,
                mod_vida,
                mod_mana,
                mod_fuerza,
                mod_agilidad,
                mod_inteligencia,
                habilidad_racial
            FROM Razas
            ORDER BY id
        """)
        self.lista_razas = self.cursor.fetchall()
        return self.lista_razas
