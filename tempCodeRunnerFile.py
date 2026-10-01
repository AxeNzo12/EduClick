from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Configuración para la base de datos SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'educlick.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# RUTAS DE NAVEGACIÓN (3 NIVELES)
# ==========================================

# Nivel 1: Selección de grado escolar (Inicio)
@app.route('/')
def index():
    # Aquí renderizamos la pantalla principal con la interfaz intuitiva para niños
    return render_template('index.html')

# Nivel 2: Selección de materia
@app.route('/grado/<int:grado_id>')
def seleccion_materia(grado_id):
    conn = get_db_connection()
    # Extraemos TODAS las materias de la base de datos
    materias = conn.execute('SELECT * FROM materias').fetchall()
    conn.close()
    
    return render_template('materias.html', grado=grado_id, materias=materias)

# Nivel 3: Ejecución de la actividad conectada a la BD
@app.route('/actividad/<int:materia_id>')
def motor_actividades(materia_id):
    # Capturamos el ID de la pregunta anterior para evitar repetirla
    excluir_id = request.args.get('excluir', default=0, type=int)
    
    conn = get_db_connection()
    
    # Buscamos una pregunta aleatoria que NO sea la misma que acabamos de responder
    actividad = conn.execute(
        'SELECT * FROM actividades WHERE materia_id = ? AND id != ? ORDER BY RANDOM() LIMIT 1', 
        (materia_id, excluir_id)
    ).fetchone()
    
    # Si por alguna razón no encuentra otra, traemos cualquiera de la materia
    if actividad is None:
        actividad = conn.execute(
            'SELECT * FROM actividades WHERE materia_id = ? ORDER BY RANDOM() LIMIT 1', 
            (materia_id,)
        ).fetchone()
        
    conn.close()
    
    if actividad is None:
        return "No hay actividades disponibles para esta materia.", 404
        
    opciones = actividad['opciones'].split(',')
    
    return render_template('actividad.html', materia_id=materia_id, actividad=actividad, opciones=opciones)


# ==========================================
# MÓDULO DE ADMINISTRADOR
# ==========================================
@app.route('/admin', methods=['GET', 'POST'])
def panel_admin():
    conn = get_db_connection()
    mensaje = None
    
    if request.method == 'POST':
        # Capturar los datos enviados desde el formulario HTML
        materia_id = request.form['materia_id']
        grado = request.form['grado']
        pregunta = request.form['pregunta']
        opciones = request.form['opciones']
        respuesta_correcta = request.form['respuesta_correcta']
        
        # Insertar la nueva actividad en SQLite
        conn.execute(
            'INSERT INTO actividades (materia_id, grado, pregunta, opciones, respuesta_correcta) VALUES (?, ?, ?, ?, ?)',
            (materia_id, grado, pregunta, opciones, respuesta_correcta)
        )
        conn.commit()
        mensaje = "¡Actividad guardada exitosamente en la base de datos!"

    # Consultar las materias para llenar el menú desplegable del formulario
    materias = conn.execute('SELECT * FROM materias').fetchall()
    conn.close()
    
    return render_template('admin.html', materias=materias, mensaje=mensaje)

# Motor Lógico: Validación real y registro de puntos contra la BD
@app.route('/api/validar_respuesta', methods=['POST'])
def validar_respuesta():
    data = request.get_json()
    respuesta_usuario = str(data.get('respuesta')).strip()
    actividad_id = data.get('actividad_id')
    
    conn = get_db_connection()
    actividad = conn.execute('SELECT respuesta_correcta FROM actividades WHERE id = ?', (actividad_id,)).fetchone()
    
    es_correcta = False
    puntos_totales = 0
    
    if actividad and respuesta_usuario == str(actividad['respuesta_correcta']):
        es_correcta = True
        
        # ID del usuario por defecto (Estudiante 1)
        usuario_id = 1 
        
        # Registrar el avance en la tabla progreso
        conn.execute(
            'INSERT INTO progreso (usuario_id, actividad_id, completado) VALUES (?, ?, 1)',
            (usuario_id, actividad_id)
        )
        conn.commit()
    
    # Consultar cuántos puntos (actividades completadas) lleva acumulados el usuario
    resultado_puntos = conn.execute(
        'SELECT COUNT(*) as total FROM progreso WHERE usuario_id = ?', 
        (1,)
    ).fetchone()
    puntos_totales = resultado_puntos['total']
    
    conn.close()
    
    return jsonify({
        'correcta': es_correcta,
        'mensaje': '¡Excelente trabajo! Ganaste 1 punto 🌟' if es_correcta else 'Inténtalo de nuevo ❌',
        'puntos': puntos_totales
    })

if __name__ == '__main__':
    # Modo debug activado para pruebas en el entorno de programación
    app.run(debug=True, port=5000)