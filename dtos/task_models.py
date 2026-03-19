from typing import Optional
from pydantic import BaseModel

class TaskModel(BaseModel):
    title :str
    description:str
    caseId:int
    status:str
    priority:str

class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    caseId: Optional[int] = None
    assignedTo: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None  
