class User:
    def __init__(self, id=None, nombre=None, email=None):
        self.id = id
        self.nombre = nombre
        self.email = email
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=str(data.get('_id')) if data.get('_id') else data.get('id'),
            nombre=data.get('nombre'),
            email=data.get('email')
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email
        }
    def to_mongo_dict(self):
        """Para guardar en MongoDB (sin el id)"""
        return {
            'nombre': self.nombre,
            'email': self.email
        }