import os

class Config:
    SECRET_KEY = 'tu_clave_secreta_aqui'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://asistentev01:Mikiztli1@asistentev01.mysql.pythonanywhere-services.com/asistentev01$usuarios'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")