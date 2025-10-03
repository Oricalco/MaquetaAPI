class User:
    def __init__(self, id=None, name=None, email=None):
        self.id = id
        self.name = name
        self.email = email
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=str(data.get('_id')) if data.get('_id') else data.get('id'),
            name=data.get('name'),
            email=data.get('email')
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
    def to_mongo_dict(self):
        """Para guardar en MongoDB (sin el id)"""
        return {
            'name': self.name,
            'email': self.email
        }