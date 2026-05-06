from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from models.logic import Guerrero, Mago
from database.personajeDAO import PersonajeDAO
from database.HabilidadDAO import HabilidadDAO
from database.InventarioDAO import InventarioDAO
from database.conexion_db import conexion_db
from models.Personaje import Personaje

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")


# ============================================================
# 🌐 RUTA PRINCIPAL
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/personajes')
def api_personajes():
    """
    Esta ruta no devuelve una página web (HTML), devuelve DATOS puros.
    Es útil para que JavaScript o herramientas externas lean tu base de datos.
    """
    #
    datos = Personaje.obtener_personajes(get_db_connection)
    return jsonify(datos)

# ============================================================
# 🚀 ARRANCAR EL SERVIDOR
# ============================================================

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
