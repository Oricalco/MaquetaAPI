from flask import Blueprint
from aplicacion.controlador.controlador_usuario import UserController
from aplicacion.servicio.servicio_usuario import UserService
from infraestructura.db.implementacion_rep_usuario import UserRepositoryImpl
def create_user_blueprint(db_connection):
    # Inyección de dependencias
    user_repository = UserRepositoryImpl(db_connection)
    user_service = UserService(user_repository)
    user_controller = UserController(user_service)
    
    # Crear blueprint
    user_bp = Blueprint('users', __name__)
    
    # Definir rutas
    @user_bp.route('/users', methods=['POST'])
    def create_user():
        return user_controller.create_user()
    
    @user_bp.route('/users', methods=['GET'])
    def get_all_users():
        return user_controller.get_all_users()
    
    @user_bp.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        return user_controller.get_user(user_id)
    
    return user_bp