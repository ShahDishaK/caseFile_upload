from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class TaskModel(BaseModel):
    title :str
    description:str
    caseId:int
    assignedTo:int
    status:str
   

class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    caseId: Optional[int] = None
    assignedTo: Optional[int] = None
    status: Optional[str] = None