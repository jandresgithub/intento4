from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.usuario_model import Usuario
from database import db

auth_bp = Blueprint('auth', __name__)

# Ruta de inicio de sesión
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    mensaje = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Buscar usuario en la base de datos
        usuario = Usuario.query.filter_by(nombre=username).first()

        if usuario and usuario.password == password:
            session['user_id'] = usuario.id
            
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('asistencias.listar_asistencias'))
        else:
            mensaje = 'Usuario o contraseña incorrectos.'

    return render_template('login.html', mensaje=mensaje)

# Ruta de cierre de sesión
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente.', 'success')
    return redirect(url_for('auth.login'))
