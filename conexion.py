from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['MONGO_URI'] = "mongodb+srv://davidtt083:12345qwerty@chatbot01.k9en0.mongodb.net/usuarios?retryWrites=true&w=majority&appName=chatbot01"

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

logging.basicConfig(level=logging.DEBUG)

def verify_password(stored_password, provided_password):
    try:
        return bcrypt.check_password_hash(stored_password, provided_password)
    except ValueError as e:
        if "Invalid salt" in str(e):
            logging.warning(f"Invalid salt error detected: {e}")
            if len(stored_password) != 60:
                return stored_password == provided_password
        return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            user = mongo.db.datos_usuarios.find_one({'email': request.form['email']})
            if user and verify_password(user['password'], request.form['password']):
                session['user_id'] = str(user['_id'])
                flash('Has iniciado sesión correctamente.', 'success')
                return redirect(url_for('chatbot_home'))
            else:
                flash('Correo electrónico o contraseña inválidos.', 'danger')
        except Exception as e:
            logging.error(f"Error durante el inicio de sesión: {e}", exc_info=True)
            flash('Ocurrió un error al intentar iniciar sesión.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            existing_user = mongo.db.datos_usuarios.find_one({'email': request.form['email']})
            if existing_user is None:
                hashpass = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
                mongo.db.datos_usuarios.insert_one({
                    'nombre': request.form['nombre'],
                    'email': request.form['email'],
                    'password': hashpass
                })
                flash('Registro exitoso. Por favor, inicia sesión.', 'success')
                return redirect(url_for('login'))
            flash('Ya existe un usuario con ese correo electrónico.', 'danger')
        except Exception as e:
            logging.error(f"Error durante el registro: {e}", exc_info=True)
            flash('Ocurrió un error durante el registro.', 'danger')
    return render_template('register.html')

# No ejecutamos la app aquí