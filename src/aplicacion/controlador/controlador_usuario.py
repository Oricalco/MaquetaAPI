# src/application/controllers/user_controller.py
from flask import jsonify, request
from aplicacion.servicio.servicio_usuario import UserService
from dominio.entidades.usuario import User

class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    def create_user(self):
        try:
            data = request.get_json()
            
            # Validación básica
            if not data or 'name' not in data or 'email' not in data:
                return jsonify({'error': 'Name and email are required'}), 400
            
            user = self.user_service.create_user(data)
            return jsonify(user.to_dict()), 201
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_user(self, user_id: int):
        try:
            user = self.user_service.get_user(user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify(user.to_dict()), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_all_users(self):
        try:
            users = self.user_service.get_all_users()
            users_data = [user.to_dict() for user in users]
            return jsonify(users_data), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500