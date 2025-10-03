from dominio.repositorios.repositorio_usuario import UserRepository
from dominio.entidades.usuario import User
from typing import List, Optional
from bson import ObjectId
import pymongo

class MongoDBUserRepository(UserRepository):
    # Cambiar "collection_name para cambiar de coleccion"
    def __init__(self, database, collection_name="usuarios"):
        self.collection = database[collection_name]
    
    def save(self, user: User) -> User:
        user_data = user.to_mongo_dict()
        
        if user.id:
            # Update existing user
            result = self.collection.update_one(
                {'_id': ObjectId(user.id)},
                {'$set': user_data}
            )
            if result.matched_count == 0:
                raise ValueError(f"User with id {user.id} not found")
        else:
            # Insert new user
            result = self.collection.insert_one(user_data)
            user.id = str(result.inserted_id)
        
        return user
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        try:
            result = self.collection.find_one({'_id': ObjectId(user_id)})
            if result:
                return User.from_dict(result)
            return None
        except:
            return None
    
    def find_all(self) -> List[User]:
        results = self.collection.find()
        return [User.from_dict(user) for user in results]