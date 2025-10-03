from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import Optional, List
from pymongo import MongoClient
from bson import ObjectId
import os

app = FastAPI()

mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(mongo_uri)
db = client['GPMLOCAL']
coleccion = db['precipitacionChile']
CAMPOS = [
    'timestamp', 'latitude', 'longitude', 'product', 'product_type', 
    'version', 'import_date', 'metadata', 'precipitation_data'
]

# Modelos anidados
class Metadata(BaseModel):
    time_index: Optional[int] = None
    lat_index: Optional[int] = None
    lon_index: Optional[int] = None

class PrecipitationData(BaseModel):
    precipitation: Optional[float] = None
    randomError: Optional[float] = None
    probabilityLiquidPrecipitation: Optional[float] = None
    precipitationQualityIndex: Optional[float] = None
    MWprecipitation: Optional[float] = None
    MWprecipSource: Optional[int] = None
    MWobservationTime: Optional[float] = None
    IRprecipitation: Optional[float] = None
    IRinfluence: Optional[float] = None
    precipitationUncal: Optional[float] = None

class Documento(BaseModel):
    timestamp: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    product: Optional[str] = None
    product_type: Optional[str] = None
    version: Optional[int] = None
    import_date: Optional[str] = None
    metadata: Optional[Metadata] = None
    precipitation_data: Optional[PrecipitationData] = None

# JWT Demo
SECRET = 'secret123'
def jwt_auth(authorization: str = Header(...)):
    if not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Missing or invalid token')
    token = authorization.split(' ')[1]
    if token != SECRET:
        raise HTTPException(status_code=401, detail='Invalid token')


def parse_doc(doc):
    # Convierte los subdocumentos a los modelos anidados
    doc = dict(doc)
    if 'metadata' in doc and isinstance(doc['metadata'], dict):
        doc['metadata'] = Metadata(**doc['metadata'])
    if 'precipitation_data' in doc and isinstance(doc['precipitation_data'], dict):
        doc['precipitation_data'] = PrecipitationData(**doc['precipitation_data'])
    return Documento(**{campo: doc.get(campo, None) for campo in CAMPOS})

@app.get('/documentos', response_model=List[Documento])
def get_documentos():
    docs = list(coleccion.find())
    return [parse_doc(doc) for doc in docs]


@app.get('/documentos/{doc_id}', response_model=Documento)
def get_documento(doc_id: str):
    doc = coleccion.find_one({'_id': ObjectId(doc_id)})
    if not doc:
        raise HTTPException(status_code=404, detail='Not found')
    return parse_doc(doc)


@app.post('/documentos', response_model=dict, dependencies=[Depends(jwt_auth)])
def post_documento(data: Documento):
    doc_dict = data.dict(exclude_unset=True)
    # Rellenar campos faltantes con None
    for campo in CAMPOS:
        if campo not in doc_dict:
            doc_dict[campo] = None
    # Convertir modelos anidados a dict
    if isinstance(doc_dict.get('metadata'), Metadata):
        doc_dict['metadata'] = doc_dict['metadata'].dict(exclude_unset=True)
    if isinstance(doc_dict.get('precipitation_data'), PrecipitationData):
        doc_dict['precipitation_data'] = doc_dict['precipitation_data'].dict(exclude_unset=True)
    result = coleccion.insert_one(doc_dict)
    return {'_id': str(result.inserted_id)}

# Endpoint: Buscar por producto
@app.get('/documentos/producto/{producto}', response_model=List[Documento])
def get_documentos_por_producto(producto: str):
    docs = coleccion.find({'product': producto})
    return [parse_doc(doc) for doc in docs]

# Endpoint: Buscar por rango de coordenadas
@app.get('/documentos/coordenadas', response_model=List[Documento])
def get_documentos_por_coordenadas(lat_min: float, lat_max: float, lon_min: float, lon_max: float):
    query = {
        'latitude': {'$gte': lat_min, '$lte': lat_max},
        'longitude': {'$gte': lon_min, '$lte': lon_max}
    }
    docs = coleccion.find(query)
    return [parse_doc(doc) for doc in docs]
