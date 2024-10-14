from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from flask_bcrypt import Bcrypt
from extensions import db
from models import User

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and bcrypt.check_password_hash(user.password_hash, request.form['password']):
            session['user_id'] = user.id
            flash('Has iniciado sesión correctamente.', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Correo electrónico o contraseña inválidos.', 'danger')
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        existing_user = User.query.filter_by(email=request.form['email']).first()
        if existing_user is None:
            hashpass = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            new_user = User(nombre=request.form['nombre'], email=request.form['email'], password_hash=hashpass)
            db.session.add(new_user)
            db.session.commit()
            flash('Registro exitoso. Por favor, inicia sesión.', 'success')
            return jsonify({"success": True, "message": "Registro exitoso"})
           
        flash('Ya existe un usuario con ese correo electrónico.', 'danger')
    return render_template('register.html')