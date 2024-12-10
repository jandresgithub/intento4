from run import app, db
from models.usuario_model import Usuario
from models.asistencia_model import Asistencia
from models.clase_model import Clase  # Importa todos los modelos que definiste

with app.app_context():
    # Crear todas las tablas en la base de datos
    db.create_all()
    print("Tablas creadas exitosamente.")
    
    # Crear un usuario administrador inicial
    if not Usuario.query.filter_by(nombre='admin').first():  # Evitar duplicados
        usuario = Usuario(nombre='admin', email='admin@example.com', password='admin123')
        db.session.add(usuario)
        db.session.commit()
        print('Usuario admin creado con éxito.')
    else:
        print('El usuario admin ya existe.')
