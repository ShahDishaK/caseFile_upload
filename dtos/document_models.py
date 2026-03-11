from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class DocumentModel(BaseModel):
    title :str
    documentLink :str
    fileType :str
    caseId :str
    userId : Optional[int] = None


class UpdateDocumentRequest(BaseModel):
    title: Optional[str] = None
    documentLink: Optional[str] = None
    fileType: Optional[str] = None
    caseId: Optional[str] = None