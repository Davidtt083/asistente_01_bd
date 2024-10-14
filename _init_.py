from flask import Flask
from config import Config
from extensions import db
from app.auth.routes import auth
from app.main.routes import main
from app.chatbot.routes import chatbot

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(chatbot)

    return app