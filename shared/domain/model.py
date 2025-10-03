from typing import Optional, Dict, Any

class Documento:
    def __init__(self, data: Dict[str, Any], campos: Optional[list] = None):
        if campos is None:
            campos = list(data.keys())
        for campo in campos:
            setattr(self, campo, data.get(campo, None))
        self._campos = campos

    def to_dict(self):
        return {campo: getattr(self, campo, None) for campo in self._campos}
