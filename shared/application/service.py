from shared.infrastructure.repository import DocumentoRepository
from shared.domain.model import Documento
from typing import List, Dict, Any, Optional

class DocumentoService:
    def __init__(self, repo: DocumentoRepository):
        self.repo = repo

    def listar_documentos(self) -> List[Documento]:
        return self.repo.get_all()

    def obtener_documento(self, doc_id: str) -> Optional[Documento]:
        return self.repo.get_by_id(doc_id)

    def crear_documento(self, data: Dict[str, Any]) -> str:
        return self.repo.create(data)
