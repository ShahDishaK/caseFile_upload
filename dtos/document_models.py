from typing import Optional
from pydantic import BaseModel

class DocumentModel(BaseModel):
    title :str
    documentLink :str
    fileType :str
    description: Optional[str] = None
    notes: Optional[str] = None
    caseId :int
    clientId : Optional[int] = None

class UpdateDocumentRequest(BaseModel):
    title: Optional[str] = None
    documentLink: Optional[str] = None
    fileType: Optional[str] = None
    caseId: Optional[int] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    clientId: Optional[int] = None