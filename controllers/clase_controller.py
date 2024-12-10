from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.clase_model import Clase
from database import db

# Crear el Blueprint
clase_bp = Blueprint('clases', __name__)

# Ruta para listar las clases
@clase_bp.route('/')
def listar_clases():
    clases = Clase.query.all()
    return render_template('clase/index.html', clases=clases)

# Ruta para mostrar el formulario de creación
@clase_bp.route('/crear', methods=['GET', 'POST'])
def crear_clase():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form.get('descripcion', '')

        nueva_clase = Clase(nombre=nombre, descripcion=descripcion)
        db.session.add(nueva_clase)
        db.session.commit()

        flash('Clase creada exitosamente.', 'success')
        return redirect(url_for('clases.listar_clases'))

    return render_template('clase/create.html')

# Ruta para editar una clase
@clase_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_clase(id):
    clase = Clase.query.get_or_404(id)

    if request.method == 'POST':
        clase.nombre = request.form['nombre']
        clase.descripcion = request.form.get('descripcion', '')
        db.session.commit()

        flash('Clase actualizada exitosamente.', 'success')
        return redirect(url_for('clases.listar_clases'))

    return render_template('clase/edit.html', clase=clase)

# Ruta para eliminar una clase
@clase_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_clase(id):
    clase = Clase.query.get_or_404(id)
    db.session.delete(clase)
    db.session.commit()

    flash('Clase eliminada exitosamente.', 'success')
    return redirect(url_for('clases.listar_clases'))
