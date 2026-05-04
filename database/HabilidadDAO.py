from database.conexion_db import ConexionDB

class HabilidadDAO(ConexionDB):

    def obtener_nivel_actual(self, id_personaje, id_habilidad):
        """Devuelve el nivel que tiene un personaje en una habilidad."""
        self.cursor.execute("""
            SELECT nivel_actual FROM Personajes_Habilidades
            WHERE id_personaje = %s AND id_habilidad = %s
        """, (id_personaje, id_habilidad))

        resultado = self.cursor.fetchone()
        return resultado[0] if resultado else 0

    def cumple_requisitos(self, id_personaje, id_habilidad):
        """Comprueba si el personaje cumple los prerequisitos."""
        self.cursor.execute("""
            SELECT id_requisito, nivel_requisito_necesario
            FROM Habilidades_Requisitos
            WHERE id_habilidad = %s
        """, (id_habilidad,))

        requisitos = self.cursor.fetchall()

        if not requisitos:
            return True

        for id_req, nivel_necesario in requisitos:
            nivel_que_tiene = self.obtener_nivel_actual(id_personaje, id_req)
            if nivel_que_tiene < nivel_necesario:
                return False

        return True

    def obtener_nivel_maximo(self, id_habilidad):
        """Devuelve el nivel máximo que puede tener una habilidad."""
        self.cursor.execute("""
            SELECT nivel_maximo FROM Habilidades WHERE id = %s
        """, (id_habilidad,))
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado else 5

    def subir_nivel(self, id_personaje, id_habilidad):
        """Intenta subir el nivel de una habilidad."""
        if not self.cumple_requisitos(id_personaje, id_habilidad):
            return {'ok': False, 'mensaje': 'No cumples los requisitos previos.'}

        nivel_actual = self.obtener_nivel_actual(id_personaje, id_habilidad)
        nivel_maximo = self.obtener_nivel_maximo(id_habilidad)

        if nivel_actual >= nivel_maximo:
            return {'ok': False, 'mensaje': f'Habilidad al máximo ({nivel_maximo}).'}

        nuevo_nivel = nivel_actual + 1

        self.cursor.execute("""
            INSERT INTO Personajes_Habilidades (id_personaje, id_habilidad, nivel_actual)
            VALUES (%s, %s, %s)
            ON CONFLICT (id_personaje, id_habilidad)
            DO UPDATE SET nivel_actual = %s
        """, (id_personaje, id_habilidad, nuevo_nivel, nuevo_nivel))
        self.conn.commit()

        return {'ok': True, 'mensaje': f'¡Habilidad mejorada al nivel {nuevo_nivel}! 🎉'}