from database import db

class Asistencia(db.Model):
    __tablename__ = 'asistencias'
    
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(20), nullable=False)

    estudiante = db.relationship('Estudiante', backref='asistencias')

    def __repr__(self):
        return f'<Asistencia Estudiante={self.estudiante_id} Fecha={self.fecha} Estado={self.estado}>'
