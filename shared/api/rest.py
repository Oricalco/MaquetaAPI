
from flask import Blueprint, request, jsonify
from functools import wraps
from pymongo import MongoClient
import os
from shared.infrastructure.repository import DocumentoRepository
from shared.application.service import DocumentoService

bp = Blueprint('documentos', __name__)

# Configuración MongoDB
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(mongo_uri)
db = client['GPMLOCAL']
coleccion = db['documentos']

# Definir los campos esperados (según schema.py)
CAMPOS = [
    'timestamp', 'latitude', 'longitude', 'product', 'product_type',
    'version', 'import_date', 'metadata', 'precipitation_data'
]
repo = DocumentoRepository(coleccion, CAMPOS)
servicio = DocumentoService(repo)

# JWT Demo
SECRET = 'secret123'
def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth or not auth.startswith('Bearer '):
            return jsonify({'msg': 'Missing or invalid token'}), 401
        token = auth.split(' ')[1]
        if token != SECRET:
            return jsonify({'msg': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

@bp.route('/documentos', methods=['GET'])
def get_documentos():
    docs = [d.to_dict() for d in servicio.listar_documentos()]
    return jsonify(docs)

@bp.route('/documentos/<doc_id>', methods=['GET'])
def get_documento(doc_id):
    doc = servicio.obtener_documento(doc_id)
    if doc:
        return jsonify(doc.to_dict())
    return jsonify({'msg': 'Not found'}), 404

@bp.route('/documentos', methods=['POST'])
@jwt_required
def post_documento():
    data = request.json or {}
    doc_id = servicio.crear_documento(data)
    return jsonify({'_id': doc_id}), 201

# Endpoint: Buscar por producto
@bp.route('/documentos/producto/<producto>', methods=['GET'])
def get_documentos_por_producto(producto):
    documentos = coleccion.find({'product': producto})
    docs = []
    for doc in documentos:
        docs.append({campo: doc.get(campo, None) for campo in CAMPOS})
    return jsonify(docs)

# Endpoint: Buscar por rango de coordenadas
@bp.route('/documentos/coordenadas', methods=['GET'])
def get_documentos_por_coordenadas():
    try:
        lat_min = float(request.args.get('lat_min'))
        lat_max = float(request.args.get('lat_max'))
        lon_min = float(request.args.get('lon_min'))
        lon_max = float(request.args.get('lon_max'))
    except (TypeError, ValueError):
        return jsonify({'msg': 'Parámetros inválidos'}), 400
    query = {
        'latitude': {'$gte': lat_min, '$lte': lat_max},
        'longitude': {'$gte': lon_min, '$lte': lon_max}
    }
    documentos = coleccion.find(query)
    docs = []
    for doc in documentos:
        docs.append({campo: doc.get(campo, None) for campo in CAMPOS})
    return jsonify(docs)
