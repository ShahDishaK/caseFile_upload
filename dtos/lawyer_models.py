from typing import Optional
from pydantic import BaseModel,EmailStr, constr,validator

class LawyerModel(BaseModel):
    name: str
    firstName:str
    lastName:str
    phoneNumber: Optional[constr(regex="^[0-9]{10}$")]
    gender:str
    address: Optional[str] = None
    userId :int
    specialization :str
    isBlocked :Optional[int]=0

class UpdateLawyerRequest(BaseModel):
    name: Optional[str] = None
    firstName:Optional[str] = None
    lastName:Optional[str] = None
    phoneNumber: Optional[constr(regex="^[0-9]{10}$")]
    gender:Optional[str] = None
    address: Optional[str] = None
    userId :Optional[int]=None
    specialization :Optional[str]=None
    isBlocked :Optional[int]=None