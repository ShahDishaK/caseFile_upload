from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class StaffModel(BaseModel):
    user_id :int
    caseId :int
    lawyerId:int
    taskId:int
    isBlocked:Optional[bool]=False

   

class UpdateStaffRequest(BaseModel):
    user_id :Optional[int]=None
    caseId :Optional[int]=None
    lawyerId:Optional[int]=None
    taskId:Optional[int]=None
    isBlocked:Optional[bool]=None