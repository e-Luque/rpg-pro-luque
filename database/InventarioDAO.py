from database.conexion_db import ConexionDB
from database.personajeDAO import PersonajeDAO

class InventarioDAO(ConexionDB):

    def comprar_item(self, id_personaje, nombre_item, precio):
        """Gestiona la compra de un objeto."""
        personaje_dao = PersonajeDAO()
        personaje = personaje_dao.obtener_por_id(id_personaje)
        personaje_dao.cerrar()

        if not personaje:
            return {'ok': False, 'mensaje': 'Personaje no encontrado.'}

        oro_actual = personaje[4]

        if oro_actual < precio:
            return {'ok': False, 'mensaje': f'Oro insuficiente: {oro_actual}/{precio}.'}

        nuevo_oro = oro_actual - precio

        self.cursor.execute("""
            INSERT INTO Inventario (id_personaje, nombre_item, cantidad)
            VALUES (%s, %s, 1)
            ON CONFLICT (id_personaje, nombre_item)
            DO UPDATE SET cantidad = Inventario.cantidad + 1
        """, (id_personaje, nombre_item))

        self.cursor.execute("""
            UPDATE Personajes SET oro = %s WHERE id = %s
        """, (nuevo_oro, id_personaje))

        self.conn.commit()

        return {
            'ok': True,
            'mensaje': f'Compraste {nombre_item}. Te quedan {nuevo_oro} monedas. 💰'
        }