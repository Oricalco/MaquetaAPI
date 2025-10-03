from flask import Flask
import pymongo
import dotenv
import os
from flask import jsonify
from infraestructura.api.rutas import create_user_blueprint
def check_existing_data(database):
    """Verifica qué colecciones y datos existen"""
    collections = database.list_collection_names()
    print("Colecciones disponibles:", collections)
    
    for collection_name in collections:
        collection = database[collection_name]
        count = collection.count_documents({})
        print(f"Colección '{collection_name}': {count} documentos")
        
        if count > 0:
            # Muestra algunos documentos de cada colección
            sample_docs = collection.find().limit(2)
            for doc in sample_docs:
                print(f"  Ejemplo: {doc}")

def create_app():
    app = Flask(__name__)
    
    # Configuración de MongoDB
    dotenv.load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")
    
    client = pymongo.MongoClient(mongo_uri)
    db = client["Test"]
    
    # Verificar conexión
    try:
        client.admin.command('ping')
        print("Conexión exitosa a MongoDB")
    except Exception as e:
        print(f"Error de conexión: {e}")
        raise
    print("=== VERIFICANDO DATOS EXISTENTES ===")
    check_existing_data(db)
    print("=====================================")

    # Registrar blueprints
    user_bp = create_user_blueprint(db)
    app.register_blueprint(user_bp)
    
    # Ruta de salud
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'database': 'MongoDB'})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)