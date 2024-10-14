from app import create_app
from extensions import db
from models import User  # Asegúrate de importar todos tus modelos aquí

app = create_app()

with app.app_context():
    db.create_all()
    print("Tablas creadas exitosamente.")