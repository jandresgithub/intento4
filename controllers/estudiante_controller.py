from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.estudiante_model import Estudiante
from database import db

# Crear el Blueprint
estudiante_bp = Blueprint('estudiantes', __name__, url_prefix='/estudiantes')

# Ruta para listar estudiantes
@estudiante_bp.route('/')
def listar_estudiantes():
    estudiantes = Estudiante.query.all()  # Obtener todos los estudiantes
    return render_template('estudiante/index.html', estudiantes=estudiantes)

# Ruta para mostrar el formulario de creación
@estudiante_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_estudiante():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        if not nombre or not apellido:
            flash('Por favor, completa todos los campos', 'error')
        else:
            nuevo = Estudiante(nombre=nombre, apellido=apellido)
            db.session.add(nuevo)
            db.session.commit()
            flash('Estudiante creado exitosamente', 'success')
            return redirect(url_for('estudiantes.listar_estudiantes'))
    return render_template('estudiante/create.html')

# Ruta para editar un estudiante
@estudiante_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_estudiante(id):
    estudiante = Estudiante.query.get_or_404(id)
    if request.method == 'POST':
        estudiante.nombre = request.form['nombre']
        estudiante.apellido = request.form['apellido']
        db.session.commit()
        flash('Estudiante actualizado correctamente', 'success')
        return redirect(url_for('estudiantes.listar_estudiantes'))
    return render_template('estudiante/edit.html', estudiante=estudiante)

# Ruta para eliminar un estudiante
@estudiante_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_estudiante(id):
    estudiante = Estudiante.query.get_or_404(id)
    db.session.delete(estudiante)
    db.session.commit()
    flash('Estudiante eliminado correctamente', 'success')
    return redirect(url_for('estudiantes.listar_estudiantes'))
