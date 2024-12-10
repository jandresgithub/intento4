from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.asistencia_model import Asistencia
from models.estudiante_model import Estudiante

from database import db
from datetime import datetime

# Crear el Blueprint
asistencia_bp = Blueprint('asistencias', __name__)

# Ruta para listar asistencias
@asistencia_bp.route('/')
def listar_asistencias():
    asistencias = Asistencia.query.all()
    estudiantes = {e.id: f"{e.nombre} {e.apellido}" for e in Estudiante.query.all()}
    return render_template('asistencia/index.html', asistencias=asistencias, estudiantes=estudiantes)

# Ruta para agregar una nueva asistencia
@asistencia_bp.route('/nuevo', methods=['GET', 'POST'])
def nueva_asistencia():
    estudiantes = Estudiante.query.all()
    if request.method == 'POST':
        estudiante_id = request.form['estudiante_id']
        fecha_str = request.form['fecha'] or datetime.now().strftime('%Y-%m-%d')
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()  # Convertir string a objeto date
        estado = request.form['estado']

        if not estudiante_id or not estado:
            flash('Por favor, completa todos los campos', 'error')
        else:
            nueva = Asistencia(estudiante_id=estudiante_id, fecha=fecha, estado=estado)
            db.session.add(nueva)
            db.session.commit()
            flash('Asistencia registrada exitosamente', 'success')
            return redirect(url_for('asistencias.listar_asistencias'))
    return render_template('asistencia/create.html', estudiantes=estudiantes)

# Ruta para editar una asistencia
@asistencia_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_asistencia(id):
    asistencia = Asistencia.query.get_or_404(id)
    estudiantes = Estudiante.query.all()
    if request.method == 'POST':
        asistencia.estudiante_id = request.form['estudiante_id']
        #asistencia.fecha = request.form['fecha']
        # Convierte la fecha de string a un objeto date de Python
        fecha_str = request.form['fecha']
        asistencia.fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()  # Convertir string a date
        asistencia.estado = request.form['estado']
        db.session.commit()
        flash('Asistencia actualizada correctamente', 'success')
        return redirect(url_for('asistencias.listar_asistencias'))
    return render_template('asistencia/edit.html', asistencia=asistencia, estudiantes=estudiantes)

# Ruta para eliminar una asistencia
@asistencia_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_asistencia(id):
    asistencia = Asistencia.query.get_or_404(id)
    db.session.delete(asistencia)
    db.session.commit()
    flash('Asistencia eliminada correctamente', 'success')
    return redirect(url_for('asistencias.listar_asistencias'))