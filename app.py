from flask import Flask, render_template, request, redirect, url_for, session
from EstudianteManager import EstudianteManager
from DocenteManager import DocenteManager
from CarreraManager import CarreraManager
from MateriaManager import MateriaManager
from AulaManager import AulaManager
from ClaseManager import ClaseManager
from UsuarioManager import UsuarioManager   
from functools import wraps
from capture_photo import capture_photo
import os
import subprocess
import os
import cv2
import imutils
import pyodbc
import base64


app = Flask(__name__)
app.secret_key = 'your_secret_key'

estudiante_manager = EstudianteManager()
docente_manager = DocenteManager()
carrera_manager = CarreraManager()
materia_manager = MateriaManager()
aula_manager = AulaManager()
clase_manager = ClaseManager()
usuario_manager = UsuarioManager()
#capture_photo = capture_photo()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = usuario_manager.get_user(username)
        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrap

# Rutas para navegar
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/estudiante')
@login_required
def estudiante():
    clases = clase_manager.get_clases()   
    docentes = docente_manager.get_docentes() 
    materias = materia_manager.get_materias()
    aulas = aula_manager.get_aulas() 
    estudiantes = estudiante_manager.get_estudiantes()
    carreras = carrera_manager.get_carreras()
    return render_template('estudiante.html', clases=clases, docentes=docentes, materias=materias, 
                            aulas=aulas, carreras=carreras,   estudiantes=estudiantes)

@app.route('/docente')
@login_required
def docente():
    clases = clase_manager.get_clases()   
    docentes = docente_manager.get_docentes() 
    materias = materia_manager.get_materias()
    aulas = aula_manager.get_aulas() 
    estudiantes = estudiante_manager.get_estudiantes()
    carreras = carrera_manager.get_carreras()
    return render_template('docente.html', clases=clases, docentes=docentes, materias=materias, 
                            aulas=aulas, carreras=carreras,   estudiantes=estudiantes)

@app.route('/carrera')
@login_required
def carrera():
    clases = clase_manager.get_clases()   
    docentes = docente_manager.get_docentes() 
    materias = materia_manager.get_materias()
    aulas = aula_manager.get_aulas() 
    estudiantes = estudiante_manager.get_estudiantes()
    carreras = carrera_manager.get_carreras()
    return render_template('carrera.html' , clases=clases, docentes=docentes, materias=materias, 
                            aulas=aulas, carreras=carreras,   estudiantes=estudiantes)

@app.route('/materia')
@login_required
def materia():
    clases = clase_manager.get_clases()   
    docentes = docente_manager.get_docentes() 
    materias = materia_manager.get_materias()
    aulas = aula_manager.get_aulas() 
    estudiantes = estudiante_manager.get_estudiantes()
    carreras = carrera_manager.get_carreras()
    return render_template('materia.html', clases=clases, docentes=docentes, materias=materias, 
                            aulas=aulas, carreras=carreras,   estudiantes=estudiantes)

@app.route('/aula')
@login_required
def aula():
    clases = clase_manager.get_clases()   
    docentes = docente_manager.get_docentes() 
    materias = materia_manager.get_materias()
    aulas = aula_manager.get_aulas() 
    estudiantes = estudiante_manager.get_estudiantes()
    carreras = carrera_manager.get_carreras()
    return render_template('aulas.html', clases=clases, docentes=docentes, materias=materias, 
                            aulas=aulas, carreras=carreras,   estudiantes=estudiantes)

@app.route('/clases')
@login_required
def clases():
    clases = clase_manager.get_clases()   
    docentes = docente_manager.get_docentes() 
    materias = materia_manager.get_materias()
    aulas = aula_manager.get_aulas() 
    estudiantes = estudiante_manager.get_estudiantes()
    carreras = carrera_manager.get_carreras()
    return render_template('clase.html', clases=clases, docentes=docentes, materias=materias, 
                            aulas=aulas, carreras=carreras,   estudiantes=estudiantes)

@app.route('/asistencia')
@login_required
def asistencia():
    return render_template('asistencia.html')

# Rutas para estudiantes
@app.route('/add_estudiante', methods=['POST'])
@login_required
def add_estudiante():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    estado = request.form['estado']
    foto = request.form['foto']

    # Ruta de la foto
    foto_path = f"static/fotos/{nombre}_{apellido}/rostro_0.jpg"
    estudiante_manager.add_estudiante(nombre, apellido, email, foto_path, estado)
    return redirect(url_for('estudiante'))

@app.route('/delete_estudiante/<int:estudiante_id>', methods=['POST'])
@login_required
def delete_estudiante(estudiante_id):
    estudiante_manager.delete_estudiante(estudiante_id)
    return redirect(url_for('estudiante'))

@app.route('/update_estudiante', methods=['POST'])
@login_required
def update_estudiante():
    estudiante_id = request.form['id']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    estado = request.form['estado']
    foto = request.form['foto']

    # Ruta de la foto
    if foto:
        foto_path = f"static/fotos/{nombre}_{apellido}/rostro_0.jpg"
    else:
        foto_path = None

    estudiante_manager.update_estudiante(estudiante_id, nombre, apellido, email, foto_path, estado)
    return redirect(url_for('estudiante'))

@app.route('/capture_photo', methods=['POST'])
@login_required
def capture_photo():
    data = request.json
    nombre = data['nombre']
    apellido = data['apellido']
    person_name = f"{nombre}_{apellido}"
    data_path = r'E:\proyectos finales\CONTROL-DE-ASITENCIA\static\FOTOS_PERFIL'
    person_path = os.path.join(data_path, person_name)

    if not os.path.exists(person_path):
        os.makedirs(person_path)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aux_frame = frame.copy()

        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            rostro = aux_frame[y:y + h, x:x + w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(os.path.join(person_path, f'rostro_{count}.jpg'), rostro)
            count += 1

        cv2.imshow('frame', frame)

        k = cv2.waitKey(1)
        if k == 27 or count >= 1:  # Captura una sola imagen
            break

    cap.release()
    cv2.destroyAllWindows()
    return redirect(url_for('estudiante'))

#rutas para docentes 
@app.route('/add_docente', methods=['POST'])
@login_required
def add_docente():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    foto = request.form['foto']
    estado = request.form['estado']
    docente_manager.add_docente(nombre, apellido, email, foto, estado)
    return redirect(url_for('docente'))

@app.route('/delete_docente/<int:docente_id>', methods=['POST'])
@login_required
def delete_docente(docente_id):
    docente_manager.delete_docente(docente_id)
    return redirect(url_for('docente'))

@app.route('/update_docente', methods=['POST'])
@login_required
def update_docente():
    docente_id = request.form['id']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    foto = request.form['foto']
    estado = request.form['estado']
    docente_manager.update_docente(docente_id, nombre, apellido, email, foto, estado)
    return redirect(url_for('docente'))

# carrera funciona
@app.route('/add_carrera', methods=['POST'])
@login_required
def add_carrera():
    nombre = request.form['nombre']
    estado = request.form['estado']
    carrera_manager.add_carrera(nombre, estado)
    return redirect(url_for('carrera'))

@app.route('/delete_carrera/<int:carrera_id>', methods=['POST'])
@login_required
def delete_carrera(carrera_id):
    carrera_manager.delete_carrera(carrera_id)
    return redirect(url_for('carrera'))

@app.route('/update_carrera', methods=['POST'])
@login_required
def update_carrera():
    carrera_id = request.form['id']
    nombre = request.form['nombre']
    estado = request.form['estado']
    carrera_manager.update_carrera(carrera_id, nombre, estado)
    return redirect(url_for('carrera'))


#materi 
@app.route('/add_materia', methods=['POST'])
@login_required
def add_materia():
    nombre = request.form['nombre']
    carrera_id = request.form['carrera_id']
    estado = request.form['estado']
    materia_manager.add_materia(nombre, carrera_id, estado)
    return redirect(url_for('materia'))

@app.route('/delete_materia/<int:materia_id>', methods=['POST'])
@login_required
def delete_materia(materia_id):
    materia_manager.delete_materia(materia_id)
    return redirect(url_for('materia'))

@app.route('/update_materia', methods=['POST'])
@login_required
def update_materia():
    materia_id = request.form['id']
    nombre = request.form['nombre']
    carrera_id = request.form['carrera_id']
    estado = request.form['estado']
    materia_manager.update_materia(materia_id, nombre, carrera_id, estado)
    return redirect(url_for('materia'))


# aulas 
@app.route('/add_aula', methods=['POST'])
@login_required
def add_aula():
    nombre = request.form['nombre']
    ubicacion = request.form['ubicacion']
    estado = request.form['estado']
    aula_manager.add_aula(nombre, ubicacion, estado)
    return redirect(url_for('aula'))

@app.route('/delete_aula/<int:aula_id>', methods=['POST'])
@login_required
def delete_aula(aula_id):
    aula_manager.delete_aula(aula_id)
    return redirect(url_for('aula'))

@app.route('/update_aula', methods=['POST'])
@login_required
def update_aula():
    aula_id = request.form['id']
    nombre = request.form['nombre']
    ubicacion = request.form['ubicacion']
    estado = request.form['estado']
    aula_manager.update_aula(aula_id, nombre, ubicacion, estado)
    return redirect(url_for('aula'))

#clase 
@app.route('/add_clase', methods=['POST'])
@login_required
def add_clase():
    materia_id = request.form['materia_id']
    docente_id = request.form['docente_id']
    aula_id = request.form['aula_id']
    horario = request.form['horario']
    estado = request.form['estado']
    clase_manager.add_clase(materia_id, docente_id, aula_id, horario, estado)
    return redirect(url_for('clases'))

@app.route('/delete_clase/<int:clase_id>', methods=['POST'])
@login_required
def delete_clase(clase_id):
    clase_manager.delete_clase(clase_id)
    return redirect(url_for('clases'))

@app.route('/update_clase', methods=['POST'])
@login_required
def update_clase():
    clase_id = request.form['id']
    materia_id = request.form['materia_id']
    docente_id = request.form['docente_id']
    aula_id = request.form['aula_id']
    horario = request.form['horario']
    estado = request.form['estado']
    clase_manager.update_clase(clase_id, materia_id, docente_id, aula_id, horario, estado)
    return redirect(url_for('clases'))


if __name__ == '__main__':
    app.run(debug=True)
