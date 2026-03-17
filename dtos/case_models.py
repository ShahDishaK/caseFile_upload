from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class CaseModel(BaseModel):
    caseNumber :int
    title :str 
    type:str
    description : str
    status: str
    caseClosedDate: Optional[datetime] = None
    caseStage:str
    caseCity:str
    clientId: Optional[int] = None
   
class UpdateCaseRequest(BaseModel):
    caseNumber: Optional[int] = None
    title: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    staffId: Optional[int] = None
    status: Optional[str] = None
    caseCloseDate: Optional[datetime] = None
    clientId: Optional[int] = None
    lawyerId: Optional[int] = None