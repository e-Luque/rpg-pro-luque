from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from models.logic import Guerrero, Mago
from database.personajeDAO import PersonajeDAO
from database.HabilidadDAO import HabilidadDAO
from database.InventarioDAO import InventarioDAO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")


# ============================================================
# 🌐 RUTA PRINCIPAL
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


# ============================================================
# ⚔️ TAREA 1: Validar árbol de habilidades y subir nivel
# ============================================================
# Cuando el jugador pulsa "Mejorar Habilidad" en el navegador,
# el JS manda un evento 'mejorar_habilidad' con el id del personaje y la habilidad.

@socketio.on('mejorar_habilidad')
def mejorar_habilidad(data):
    """
    data = { 'id_personaje': 1, 'id_habilidad': 2 }
    """
    data = data or {}
    id_personaje = data.get('id_personaje')
    id_habilidad = data.get('id_habilidad')

    if not id_personaje or not id_habilidad:
        emit('status', {'ok': False, 'mensaje': 'Faltan datos: necesito id_personaje e id_habilidad.'})
        return

    # Usamos el DAO para hacer todo el trabajo sucio
    dao = HabilidadDAO()
    resultado = dao.subir_nivel(id_personaje, id_habilidad)
    dao.cerrar()

    # Mandamos la respuesta al cliente
    emit('status', resultado)


# ============================================================
# 💥 TAREA 2: Cálculo de daño dinámico según clase y nivel
# ============================================================
# El daño depende del nivel del personaje y del multiplicador de su clase.
#   - Guerrero: daño = nivel × 10 × 1.5
#   - Mago:     daño = nivel × 10 × 2.0

@socketio.on('atacar')
def atacar(data):
    """
    data = { 'id_personaje': 1, 'id_objetivo': 2 }
    """
    data = data or {}
    id_personaje = data.get('id_personaje')
    id_objetivo  = data.get('id_objetivo')

    if not id_personaje or not id_objetivo:
        emit('status', {'ok': False, 'mensaje': 'Faltan datos: necesito id_personaje e id_objetivo.'})
        return

    # Sacamos los datos del personaje que ataca
    dao = PersonajeDAO()
    fila_atacante = dao.obtener_por_id(id_personaje)
    fila_objetivo = dao.obtener_por_id(id_objetivo)

    if not fila_atacante or not fila_objetivo:
        dao.cerrar()
        emit('status', {'ok': False, 'mensaje': 'No se encontró el personaje o el objetivo.'})
        return

    # Reconstruimos el objeto Python a partir de los datos de la BD
    # fila = (id, nombre, nivel, exp, oro, vida_actual, raza, clase)
    nombre_clase = fila_atacante[7]
    nivel        = fila_atacante[2]

    # Elegimos la clase correcta según lo que devuelve la BD
    if nombre_clase == 'Guerrero':
        clase_obj = Guerrero()
    elif nombre_clase == 'Mago':
        clase_obj = Mago()
    else:
        # Si hay otra clase no definida, ponemos daño base
        clase_obj = None

    # Calculamos el daño base: nivel × 10
    daño_base = nivel * 10

    # Aplicamos el multiplicador de la clase
    if isinstance(clase_obj, Guerrero):
        daño_final = int(daño_base * clase_obj.multiplicador_daño)
    elif isinstance(clase_obj, Mago):
        daño_final = int(daño_base * clase_obj.multiplicador_magico)
    else:
        daño_final = daño_base

    # Calculamos la nueva vida del objetivo
    vida_objetivo = fila_objetivo[5]
    nueva_vida    = max(0, vida_objetivo - daño_final)  # La vida no puede bajar de 0

    # Actualizamos la vida en la base de datos
    dao.actualizar_vida(id_objetivo, nueva_vida)
    dao.cerrar()

    emit('resultado_ataque', {
        'ok': True,
        'atacante': fila_atacante[1],
        'objetivo': fila_objetivo[1],
        'daño': daño_final,
        'vida_restante': nueva_vida,
        'mensaje': f'{fila_atacante[1]} hace {daño_final} de daño. Al objetivo le quedan {nueva_vida} de vida. ⚔️'
    })


# ============================================================
# 🛒 TAREA 3: Gestión de inventario (comprar ítems)
# ============================================================

@socketio.on('comprar_item')
def comprar_item(data):
    """
    data = { 'id_personaje': 1, 'nombre_item': 'Poción de Vida', 'precio': 50 }
    """
    data = data or {}
    id_personaje = data.get('id_personaje')
    nombre_item  = data.get('nombre_item')
    precio       = data.get('precio')

    if not id_personaje or not nombre_item or precio is None:
        emit('status', {'ok': False, 'mensaje': 'Faltan datos para la compra.'})
        return

    dao = InventarioDAO()
    resultado = dao.comprar_item(id_personaje, nombre_item, precio)
    dao.cerrar()

    emit('status', resultado)


# ============================================================
# 🚀 ARRANCAR EL SERVIDOR
# ============================================================

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
