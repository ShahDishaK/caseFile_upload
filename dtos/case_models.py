from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class CaseModel(BaseModel):
    caseNumber :int
    title :str 
    type:str
    description : str
    staffId:int
    status: str
   
class UpdateCaseRequest(BaseModel):
    caseNumber: Optional[int] = None
    title: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    staffId: Optional[int] = None
    status: Optional[str] = None