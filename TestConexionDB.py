import pymongo
import dotenv
import os
dotenv.load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
print("Mongo URI:", mongo_uri)
# Nueva configuración de MongoDB
client = pymongo.MongoClient(
    mongo_uri
)
db = client["ColeccionTest"]
db = client["precipitacionChile"]

# Para verificar la conexión
try:
    client.admin.command('ping')
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error de conexión: {e}")
