# __init__.py
from flask import Flask
from config import Config
from extensions import mongo
from app.auth.routes import auth
from app.main.routes import main
from app.chatbot.routes import chatbot

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='templates')
    app.config.from_object(config_class)

    mongo.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(chatbot)

    return app