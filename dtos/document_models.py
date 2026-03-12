from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class DocumentModel(BaseModel):
    title :str
    documentLink :str
    fileType :str
    description: Optional[str] = None
    notes: Optional[str] = None
    caseId :int
    userId : Optional[int] = None
    clientId : Optional[int] = None


class UpdateDocumentRequest(BaseModel):
    title: Optional[str] = None
    documentLink: Optional[str] = None
    fileType: Optional[str] = None
    caseId: Optional[int] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    clientId: Optional[int] = None