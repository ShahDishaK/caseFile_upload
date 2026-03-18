from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class LawyerModel(BaseModel):
    userId :int
    specialization :str
    isBlocked :Optional[int]=0


class UpdateLawyerRequest(BaseModel):
    userId :Optional[int]=None
    specialization :Optional[str]=None
    isBlocked :Optional[int]=0