from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
# Clave secreta OBLIGATORIA para guardar las sesiones de los estudiantes
app.secret_key = 'educlick_clave_secreta_segura' 

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'educlick.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# RUTAS DE NAVEGACIÓN Y ACCESO
# ==========================================

# 1. Inicio: Registro de Nombre
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre').strip()
        if nombre_usuario:
            conn = get_db_connection()
            usuario = conn.execute('SELECT * FROM usuarios WHERE nombre = ?', (nombre_usuario,)).fetchone()
            
            if usuario:
                usuario_id = usuario['id']
            else:
                cursor = conn.execute('INSERT INTO usuarios (nombre, grado) VALUES (?, 1)', (nombre_usuario,))
                conn.commit()
                usuario_id = cursor.lastrowid
            
            conn.close()
            
            session['usuario_id'] = usuario_id
            session['usuario_nombre'] = nombre_usuario
            
            return redirect(url_for('seleccion_grado'))
            
    return render_template('index.html')

# 2. Selección de grado escolar
@app.route('/grados')
def seleccion_grado():
    if 'usuario_id' not in session:
        return redirect(url_for('index'))
    return render_template('grados.html')

# 3. Selección de materia
@app.route('/grado/<int:grado_id>')
def seleccion_materia(grado_id):
    if 'usuario_id' not in session:
        return redirect(url_for('index'))
        
    conn = get_db_connection()
    materias = conn.execute('SELECT * FROM materias').fetchall()
    conn.close()
    
    return render_template('materias.html', grado=grado_id, materias=materias)

# 4. Motor de actividades (¡Filtra preguntas ya contestadas!)
@app.route('/actividad/<int:grado_id>/<int:materia_id>')
def motor_actividades(grado_id, materia_id):
    if 'usuario_id' not in session:
        return redirect(url_for('index'))
        
    usuario_id = session['usuario_id']
    
    conn = get_db_connection()
    
    # Consultar los puntos reales acumulados
    res_puntos = conn.execute('SELECT COUNT(*) as total FROM progreso WHERE usuario_id = ?', (usuario_id,)).fetchone()
    puntos_actuales = res_puntos['total'] if res_puntos else 0
    
    # MAGIA: Seleccionar pregunta que NO esté en el progreso de este usuario
    actividad = conn.execute('''
        SELECT * FROM actividades 
        WHERE materia_id = ? AND grado = ? 
        AND id NOT IN (SELECT actividad_id FROM progreso WHERE usuario_id = ?)
        ORDER BY RANDOM() LIMIT 1
    ''', (materia_id, grado_id, usuario_id)).fetchone()
        
    conn.close()
    
    # Si actividad es None, significa que YA ACABÓ TODAS las de esa materia
    if actividad is None:
        return render_template(
            'completado.html', 
            grado_id=grado_id, 
            puntos=puntos_actuales, 
            nombre_usuario=session.get('usuario_nombre')
        )
        
    opciones = actividad['opciones'].split(',')
    
    return render_template(
        'actividad.html', 
        grado_id=grado_id,
        materia_id=materia_id, 
        actividad=actividad, 
        opciones=opciones, 
        puntos=puntos_actuales,
        nombre_usuario=session.get('usuario_nombre')
    )

# 5. Validación de respuesta interactiva
@app.route('/api/validar_respuesta', methods=['POST'])
def validar_respuesta():
    if 'usuario_id' not in session:
        return jsonify({'correcta': False, 'mensaje': 'Sesión expirada'}), 401
        
    data = request.get_json()
    respuesta_usuario = str(data.get('respuesta')).strip()
    actividad_id = data.get('actividad_id')
    usuario_id = session['usuario_id']
    
    conn = get_db_connection()
    actividad = conn.execute('SELECT respuesta_correcta FROM actividades WHERE id = ?', (actividad_id,)).fetchone()
    
    es_correcta = False
    
    if actividad and respuesta_usuario == str(actividad['respuesta_correcta']):
        es_correcta = True
        
        ya_contestada = conn.execute(
            'SELECT * FROM progreso WHERE usuario_id = ? AND actividad_id = ?',
            (usuario_id, actividad_id)
        ).fetchone()
        
        if not ya_contestada:
            conn.execute('INSERT INTO progreso (usuario_id, actividad_id, completado) VALUES (?, ?, 1)', (usuario_id, actividad_id))
            conn.commit()
    
    resultado_puntos = conn.execute('SELECT COUNT(*) as total FROM progreso WHERE usuario_id = ?', (usuario_id,)).fetchone()
    puntos_totales = resultado_puntos['total']
    
    conn.close()
    
    return jsonify({
        'correcta': es_correcta,
        'mensaje': '¡Excelente trabajo! 🌟' if es_correcta else 'Inténtalo de nuevo ❌',
        'puntos': puntos_totales
    })

# ==========================================
# MÓDULO DE ADMINISTRADOR
# ==========================================
@app.route('/admin', methods=['GET', 'POST'])
def panel_admin():
    conn = get_db_connection()
    mensaje = None
    
    if request.method == 'POST':
        materia_id = request.form['materia_id']
        grado = request.form['grado']
        pregunta = request.form['pregunta']
        opciones = request.form['opciones']
        respuesta_correcta = request.form['respuesta_correcta']
        
        conn.execute(
            'INSERT INTO actividades (materia_id, grado, pregunta, opciones, respuesta_correcta) VALUES (?, ?, ?, ?, ?)',
            (materia_id, grado, pregunta, opciones, respuesta_correcta)
        )
        conn.commit()
        mensaje = "¡Actividad guardada exitosamente!"

    materias = conn.execute('SELECT * FROM materias').fetchall()
    conn.close()
    
    return render_template('admin.html', materias=materias, mensaje=mensaje)

# ==========================================
# CERRAR SESIÓN
# ==========================================
@app.route('/logout')
def logout():
    # Esto borra el usuario y los puntos de la memoria del navegador
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)