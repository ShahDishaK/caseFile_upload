from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class LawyerModel(BaseModel):
    userId :int
    specialization :str
    caseId :int
    isBlocked :Optional[bool]=False


class UpdateLawyerRequest(BaseModel):
    userId :Optional[int]=None
    specialization :Optional[str]=None
    caseId :Optional[int]=None