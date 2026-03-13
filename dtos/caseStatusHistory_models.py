from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class CaseStatusHistoryModel(BaseModel):
    caseId :int
    oldStatus :str 
    newStatus:str
      
class UpdateCaseStatusHistoryRequest(BaseModel):
    caseId: Optional[int] = None
    oldStatus: Optional[str] = None
    newStatus: Optional[str] = None
   