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
        """Comprueba si los requisitos previos estan al nivel maximo."""
        self.cursor.execute("""
            SELECT hr.id_requisito, h.nivel_maximo
            FROM Habilidades_Requisitos hr
            JOIN Habilidades h ON h.id = hr.id_requisito
            WHERE hr.id_habilidad = %s
        """, (id_habilidad,))

        requisitos = self.cursor.fetchall()

        if not requisitos:
            return True

        for id_req, nivel_necesario in requisitos:
            nivel_que_tiene = self.obtener_nivel_actual(id_personaje, id_req)
            if nivel_que_tiene < nivel_necesario:
                return False

        return True

    def obtener_arbol(self, id_personaje):
        """Devuelve las habilidades del personaje con sus requisitos de desbloqueo."""
        self.cursor.execute("""
            SELECT
                h.id,
                h.nombre,
                h.descripcion,
                h.tipo,
                h.nivel_maximo,
                h.costo_mana,
                h.dano_base,
                c.nombre AS clase,
                COALESCE(ph.nivel_actual, 0) AS nivel_actual,
                req.id AS requisito_id,
                req.nombre AS requisito_nombre,
                req.nivel_maximo AS requisito_nivel_maximo,
                COALESCE(req_ph.nivel_actual, 0) AS requisito_nivel_actual
            FROM Personajes p
            JOIN Habilidades h ON h.id_clase = p.id_clase OR h.id_clase IS NULL
            LEFT JOIN Clases_RPG c ON c.id = h.id_clase
            LEFT JOIN Personajes_Habilidades ph
                ON ph.id_personaje = p.id AND ph.id_habilidad = h.id
            LEFT JOIN Habilidades_Requisitos hr ON hr.id_habilidad = h.id
            LEFT JOIN Habilidades req ON req.id = hr.id_requisito
            LEFT JOIN Personajes_Habilidades req_ph
                ON req_ph.id_personaje = p.id AND req_ph.id_habilidad = req.id
            WHERE p.id = %s
            ORDER BY h.id, req.id
        """, (id_personaje,))

        habilidades = {}

        for fila in self.cursor.fetchall():
            (
                id_habilidad,
                nombre,
                descripcion,
                tipo,
                nivel_maximo,
                costo_mana,
                dano_base,
                clase,
                nivel_actual,
                requisito_id,
                requisito_nombre,
                requisito_nivel_maximo,
                requisito_nivel_actual,
            ) = fila

            if id_habilidad not in habilidades:
                habilidades[id_habilidad] = {
                    'id': id_habilidad,
                    'nombre': nombre,
                    'descripcion': descripcion,
                    'tipo': tipo,
                    'nivel_maximo': nivel_maximo,
                    'costo_mana': costo_mana,
                    'dano_base': dano_base,
                    'clase': clase or 'General',
                    'nivel_actual': nivel_actual,
                    'requisitos': [],
                }

            if requisito_id is not None:
                habilidades[id_habilidad]['requisitos'].append({
                    'id': requisito_id,
                    'nombre': requisito_nombre,
                    'nivel_actual': requisito_nivel_actual,
                    'nivel_necesario': requisito_nivel_maximo,
                    'cumplido': requisito_nivel_actual >= requisito_nivel_maximo,
                })

        arbol = []
        for habilidad in habilidades.values():
            requisitos = habilidad['requisitos']
            desbloqueada = all(req['cumplido'] for req in requisitos)
            habilidad['desbloqueada'] = desbloqueada
            habilidad['puede_subir'] = desbloqueada and habilidad['nivel_actual'] < habilidad['nivel_maximo']
            arbol.append(habilidad)

        return arbol

    def obtener_nivel_maximo(self, id_habilidad):
        """Devuelve el nivel m�ximo que puede tener una habilidad."""
        self.cursor.execute("""
            SELECT nivel_maximo FROM Habilidades WHERE id = %s
        """, (id_habilidad,))
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado else 5

    def subir_nivel(self, id_personaje, id_habilidad):
        """Intenta subir el nivel de una habilidad."""
        if not self.cumple_requisitos(id_personaje, id_habilidad):
            return {'ok': False, 'mensaje': 'La habilidad anterior debe estar al nivel maximo.'}

        nivel_actual = self.obtener_nivel_actual(id_personaje, id_habilidad)
        nivel_maximo = self.obtener_nivel_maximo(id_habilidad)

        if nivel_actual >= nivel_maximo:
            return {'ok': False, 'mensaje': f'Habilidad al m�ximo ({nivel_maximo}).'}

        nuevo_nivel = nivel_actual + 1

        self.cursor.execute("""
            INSERT INTO Personajes_Habilidades (id_personaje, id_habilidad, nivel_actual)
            VALUES (%s, %s, %s)
            ON CONFLICT (id_personaje, id_habilidad)
            DO UPDATE SET nivel_actual = %s
        """, (id_personaje, id_habilidad, nuevo_nivel, nuevo_nivel))
        self.conn.commit()

        return {'ok': True, 'mensaje': f'Habilidad mejorada al nivel {nuevo_nivel}.'}


