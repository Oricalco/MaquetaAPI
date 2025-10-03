from pymongo.collection import Collection
from typing import List, Dict, Any, Optional
from shared.domain.model import Documento

class DocumentoRepository:
    def __init__(self, collection: Collection, campos: Optional[list] = None):
        self.collection = collection
        self.campos = campos

    def get_all(self) -> List[Documento]:
        docs = list(self.collection.find())
        return [Documento(doc, self.campos) for doc in docs]

    def get_by_id(self, doc_id: str) -> Optional[Documento]:
        from bson import ObjectId
        doc = self.collection.find_one({'_id': ObjectId(doc_id)})
        if doc:
            return Documento(doc, self.campos)
        return None

    def create(self, data: Dict[str, Any]) -> str:
        # Rellenar campos faltantes con None
        if self.campos:
            for campo in self.campos:
                if campo not in data:
                    data[campo] = None
        result = self.collection.insert_one(data)
        return str(result.inserted_id)
