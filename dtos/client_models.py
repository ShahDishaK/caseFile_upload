from typing import Optional
from pydantic import BaseModel, constr

class ClientModel(BaseModel):
    name: str
    firstName:str
    lastName:str
    phoneNumber: Optional[constr(regex="^[0-9]{10}$")]
    gender:str
    address: Optional[str] = None
    crNumber:int
    vatNumber:int
    vatPercentage:int
    occupation:str
    userId:int
    isDeleted: Optional[int] = False
    isBlocked: Optional[int] = False
    
class UpdateClientRequest(BaseModel):
    name: Optional[str] = None
    firstName:Optional[str] = None
    lastName:Optional[str] = None
    phoneNumber: Optional[constr(regex="^[0-9]{10}$")]
    gender:Optional[str] = None
    address: Optional[str] = None
    crNumber:Optional[int]=None
    vatNumber:Optional[int]=None
    vatPercentage:Optional[int]=None
    occupation:Optional[str]=None
    userId:Optional[str]=None
    lawyerId :Optional[int]=None
    isDeleted: Optional[int] = None
    isBlocked: Optional[int] = None