from dominio.repositorios.repositorio_usuario import UserRepository
from dominio.entidades.usuario import User
from typing import List, Optional

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def create_user(self, user_data: dict) -> User:
        user = User.from_dict(user_data)
        return self.user_repository.save(user)
    
    def get_user(self, user_id: str) -> Optional[User]:
        return self.user_repository.find_by_id(user_id)
    
    def get_all_users(self) -> List[User]:
        return self.user_repository.find_all()