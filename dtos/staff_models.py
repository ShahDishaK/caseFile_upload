from typing import Optional
from pydantic import BaseModel

class StaffModel(BaseModel):
    user_id :int
    caseId :int
    lawyerId:int
    isBlocked:Optional[int]=0

class UpdateStaffRequest(BaseModel):
    user_id :Optional[int]=None
    caseId :Optional[int]=None
    lawyerId:Optional[int]=None
    isBlocked:Optional[int]=None