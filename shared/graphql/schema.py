from graphene import ObjectType, String, Field, List, Mutation, Schema, ID, InputObjectType, Float, Int, Boolean
from graphene.types.generic import GenericScalar
from flask import Flask
from flask_graphql import GraphQLView
from pymongo import MongoClient
import os
from shared.infrastructure.repository import DocumentoRepository
from shared.application.service import DocumentoService

# Configuración MongoDB
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(mongo_uri)
db = client['precipitacionChile']
coleccion = db['documentos']

# Campos basados en la estructura real del documento
CAMPOS = [
    'timestamp', 'latitude', 'longitude', 'product', 'product_type', 
    'version', 'import_date', 'metadata', 'precipitation_data'
]

repo = DocumentoRepository(coleccion, CAMPOS)
servicio = DocumentoService(repo)

# Types para las estructuras anidadas
class LocationType(ObjectType):
    type = String()
    coordinates = List(Float)

class MetadataType(ObjectType):
    time_index = Int()
    lat_index = Int()
    lon_index = Int()

class PrecipitationDataType(ObjectType):
    precipitation = Float()
    randomError = Float()
    probabilityLiquidPrecipitation = Float()
    precipitationQualityIndex = Float()
    MWprecipitation = Float()
    MWprecipSource = Int()
    MWobservationTime = Float()
    IRprecipitation = Float()
    IRinfluence = Float()
    precipitationUncal = Float()

class DocumentoType(ObjectType):
    _id = ID()
    timestamp = String()
    location = Field(LocationType)
    latitude = Float()
    longitude = Float()
    product = String()
    product_type = String()
    version = Int()
    import_date = String()
    metadata = Field(MetadataType)
    precipitation_data = Field(PrecipitationDataType)

# Input Types para mutations
class LocationInput(InputObjectType):
    type = String(default_value="Point")
    coordinates = List(Float)

class MetadataInput(InputObjectType):
    time_index = Int()
    lat_index = Int()
    lon_index = Int()

class PrecipitationDataInput(InputObjectType):
    precipitation = Float()
    randomError = Float()
    probabilityLiquidPrecipitation = Float()
    precipitationQualityIndex = Float()
    MWprecipitation = Float()
    MWprecipSource = Int()
    MWobservationTime = Float()
    IRprecipitation = Float()
    IRinfluence = Float()
    precipitationUncal = Float()

class DocumentoInput(InputObjectType):
    timestamp = String()
    latitude = Float()
    longitude = Float()
    product = String()
    product_type = String()
    version = Int()
    import_date = String()
    location = LocationInput()
    metadata = MetadataInput()
    precipitation_data = PrecipitationDataInput()

# Queries
class Query(ObjectType):
    documentos = List(DocumentoType)
    documento = Field(DocumentoType, id=ID(required=True))
    documentos_por_producto = List(DocumentoType, producto=String(required=True))
    documentos_por_coordenadas = List(
        DocumentoType, 
        lat_min=Float(required=True),
        lat_max=Float(required=True),
        lon_min=Float(required=True), 
        lon_max=Float(required=True)
    )

    def resolve_documentos(root, info):
        documentos = servicio.listar_documentos()
        return [adaptar_documento_graphene(doc) for doc in documentos]

    def resolve_documento(root, info, id):
        doc = servicio.obtener_documento(id)
        if doc:
            return adaptar_documento_graphene(doc)
        return None

    def resolve_documentos_por_producto(root, info, producto):
        # Necesitarías implementar este método en tu servicio
        documentos = servicio.buscar_por_producto(producto)
        return [adaptar_documento_graphene(doc) for doc in documentos]

    def resolve_documentos_por_coordenadas(root, info, lat_min, lat_max, lon_min, lon_max):
        # Necesitarías implementar este método en tu servicio
        documentos = servicio.buscar_por_rango_coordenadas(lat_min, lat_max, lon_min, lon_max)
        return [adaptar_documento_graphene(doc) for doc in documentos]

# Mutations
class CreateDocumento(Mutation):
    class Arguments:
        input = DocumentoInput(required=True)

    ok = Boolean()
    documento = Field(DocumentoType)

    def mutate(root, info, input):
        try:
            # Convertir el input a dict y asegurar que location tenga las coordenadas
            documento_data = dict(input)
            
            # Si no se proporciona location pero sí lat/long, crear location automáticamente
            if 'location' not in documento_data and 'latitude' in documento_data and 'longitude' in documento_data:
                documento_data['location'] = {
                    'type': 'Point',
                    'coordinates': [documento_data['longitude'], documento_data['latitude']]
                }
            
            doc_id = servicio.crear_documento(documento_data)
            doc = servicio.obtener_documento(doc_id)
            
            return CreateDocumento(
                ok=True, 
                documento=adaptar_documento_graphene(doc)
            )
        except Exception as e:
            return CreateDocumento(ok=False, documento=None)

class UpdateDocumento(Mutation):
    class Arguments:
        id = ID(required=True)
        input = DocumentoInput(required=True)

    ok = Boolean()
    documento = Field(DocumentoType)

    def mutate(root, info, id, input):
        try:
            documento_data = dict(input)
            servicio.actualizar_documento(id, documento_data)
            doc = servicio.obtener_documento(id)
            
            return UpdateDocumento(
                ok=True, 
                documento=adaptar_documento_graphene(doc)
            )
        except Exception as e:
            return UpdateDocumento(ok=False, documento=None)

class DeleteDocumento(Mutation):
    class Arguments:
        id = ID(required=True)

    ok = Boolean()
    id = ID()

    def mutate(root, info, id):
        try:
            servicio.eliminar_documento(id)
            return DeleteDocumento(ok=True, id=id)
        except Exception as e:
            return DeleteDocumento(ok=False, id=None)

class Mutation(ObjectType):
    create_documento = CreateDocumento.Field()
    update_documento = UpdateDocumento.Field()
    delete_documento = DeleteDocumento.Field()

schema = Schema(query=Query, mutation=Mutation)

# Función helper para adaptar documentos a GraphQL
def adaptar_documento_graphene(documento):
    """Convierte un documento del repositorio al formato GraphQL"""
    doc_dict = documento.to_dict()
    
    # Asegurar que _id sea string
    if '_id' in doc_dict:
        doc_dict['_id'] = str(doc_dict['_id'])
    
    return DocumentoType(**doc_dict)
