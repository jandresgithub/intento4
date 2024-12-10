from flask import Flask, render_template, session, url_for, redirect
from flask_session import Session
from database import db

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de la aplicación
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///asistencia.db'  # Base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super_secreto'  # Clave para formularios

# Configuración de Flask-Session
app.config['SESSION_TYPE'] = 'sqlalchemy'  # Almacenar sesiones en la base de datos
app.config['SESSION_SQLALCHEMY'] = db     # Usar SQLAlchemy para las sesiones

# Inicializar la base de datos y Flask-Session
db.init_app(app)
Session(app)

# Importar controladores (Asegúrate de que los archivos estén creados)
from controllers.estudiante_controller import estudiante_bp
from controllers.asistencia_controller import asistencia_bp
from controllers.reporte_controller import reporte_bp
from controllers.clase_controller import clase_bp
from controllers.auth_controller import auth_bp  # Nuevo controlador de autenticación

# Registrar los Blueprints
app.register_blueprint(estudiante_bp, url_prefix='/estudiantes')
app.register_blueprint(asistencia_bp, url_prefix='/asistencias')
app.register_blueprint(reporte_bp, url_prefix='/reportes')
app.register_blueprint(clase_bp, url_prefix='/clases')
app.register_blueprint(auth_bp, url_prefix='/auth')  # Registrar el Blueprint de autenticación

# Ruta principal   #esto es el original
#@app.route('/')
#def index():
 #   return render_template('home.html')

#if __name__ == '__main__':
    # Ejecutar la aplicación en modo de desarrollo
 #   with app.app_context():
  #      db.create_all()  # Crear tablas de la base de datos
   # app.run(debug=True)
    

@app.route('/')
def index():
    # Verificar si el usuario está autenticado
    if 'user_id' not in session:
        return redirect(url_for('asistencias.listar_asistencias'))
    return redirect(url_for('auth.login'))
    
if __name__ == '__main__':
     #Ejecutar la aplicación en modo de desarrollo
    with app.app_context():
        db.create_all()  # Crear tablas de la base de datos
    app.run(debug=True)



