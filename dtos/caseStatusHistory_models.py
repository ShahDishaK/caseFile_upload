from typing import Optional
from pydantic import BaseModel

class CaseStatusHistoryModel(BaseModel):
    caseId :int
    oldStatus :str 
    newStatus:str
      
class UpdateCaseStatusHistoryRequest(BaseModel):
    oldStatus: Optional[str] = None
    newStatus: Optional[str] = None
   