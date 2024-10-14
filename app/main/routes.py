from flask import Blueprint, render_template, session, redirect, url_for
from extensions import db
from models import User  # Asegúrate de haber creado este modelo como se mostró anteriormente

main = Blueprint('main', __name__)

@main.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    if user is None:
        # Si el usuario no se encuentra, cierra la sesión y redirige al login
        session.pop('user_id', None)
        return redirect(url_for('auth.login'))
    
    return render_template('home.html', user=user)