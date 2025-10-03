# src/main.py
from flask import Flask
import sqlite3
from infraestructura.api.rutas import create_user_blueprint
def create_app():
    app = Flask(__name__)
    
    # Configuración de la base de datos
    db_connection = sqlite3.connect('your_database.db', check_same_thread=False)
    
    # Registrar blueprints
    user_bp = create_user_blueprint(db_connection)
    app.register_blueprint(user_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)