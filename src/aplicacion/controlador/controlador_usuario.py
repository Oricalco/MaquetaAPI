from flask import jsonify, request
from aplicacion.servicio.servicio_usuario import UserService
from dominio.entidades.usuario import User
from bson import ObjectId
from bson.errors import InvalidId

class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    def create_user(self):
        try:
            data = request.get_json()
            
            if not data or 'nombre' not in data or 'email' not in data:
                return jsonify({'error': 'nombre y email son necesarios'}), 400
            
            user = self.user_service.create_user(data)
            return jsonify(user.to_dict()), 201
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_user(self, user_id: str):
        try:
            user = self.user_service.get_user(user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify(user.to_dict()), 200
        
        except InvalidId:
            return jsonify({'error': 'Invalid user ID format'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_all_users(self):
        try:
            users = self.user_service.get_all_users()
            users_data = [user.to_dict() for user in users]
            return jsonify(users_data), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500