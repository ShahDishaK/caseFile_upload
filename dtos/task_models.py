from enum import Enum
from typing import Optional
from pydantic import BaseModel

class TaskStatus(str, Enum):
    TODAY = "today"
    OVERDUE = "overdue"
    COMPLETED = "completed"


class TaskModel(BaseModel):
    title :str
    description:str
    caseId:int
    status:TaskStatus
    priority:str

class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    caseId: Optional[int] = None
    assignedTo: Optional[int] = None
    status: Optional[TaskStatus] = None
    priority: Optional[str] = None  
