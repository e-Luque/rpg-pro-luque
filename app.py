from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit

from database.HabilidadDAO import HabilidadDAO
from database.conexion_db import get_db_connection

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/personajes')
def api_personajes():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, nombre, nivel, exp, oro, vida_actual, id_raza, id_clase
                FROM Personajes
                ORDER BY id
            """)
            personajes = [
                {
                    'id': fila[0],
                    'nombre': fila[1],
                    'nivel': fila[2],
                    'exp': fila[3],
                    'oro': fila[4],
                    'vida_actual': fila[5],
                    'id_raza': fila[6],
                    'id_clase': fila[7],
                }
                for fila in cursor.fetchall()
            ]

    return jsonify(personajes)

@app.route('/api/items')
def api_items():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT i.id, i.nombre, i.descripcion, i.precio, t.nombre AS tipo, i.rareza
                FROM Items i
                LEFT JOIN Tipos_Item t ON t.id = i.tipo
                ORDER BY id
            """)
            items = [
                {
                    'id': fila[0],
                    'nombre': fila[1],
                    'descripcion': fila[2],
                    'precio': fila[3],
                    'tipo': fila[4],
                    'rareza': fila[5]
                }
                for fila in cursor.fetchall()
            ]

    return jsonify(items)



@app.route('/api/habilidades/<int:id_personaje>')
def obtener_habilidades(id_personaje):
    habilidades = HabilidadDAO().obtener_arbol(id_personaje)

    return jsonify({
        "habilidades": habilidades
    })
@socketio.on('mejorar_habilidad')
def mejorar_habilidad(data):
    id_personaje = data.get('id_personaje')
    id_habilidad = data.get('id_habilidad')

    if not id_personaje or not id_habilidad:
        emit('status', {'ok': False, 'mensaje': 'Faltan datos.'})
        return

    habilidad_dao = HabilidadDAO()
    try:
        resultado = habilidad_dao.subir_nivel(id_personaje, id_habilidad)
    finally:
        habilidad_dao.cerrar()

    emit('status', resultado)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
