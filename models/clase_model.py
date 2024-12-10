from database import db

class Clase(db.Model):
    __tablename__ = 'clases'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)

    def __init__(self, nombre, descripcion=None):
        self.nombre = nombre
        self.descripcion = descripcion
