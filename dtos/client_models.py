from typing import Optional
from pydantic import BaseModel

class ClientModel(BaseModel):
    crNumber:int
    vatNumber:int
    vatPercentage:int
    occupation:str
    userId:int
    isDeleted: Optional[int] = False
    isBlocked: Optional[int] = False
    
class UpdateClientRequest(BaseModel):
    crNumber:Optional[int]=None
    vatNumber:Optional[int]=None
    vatPercentage:Optional[int]=None
    occupation:Optional[str]=None
    userId:Optional[str]=None
    lawyerId :Optional[int]=None
    isDeleted: Optional[int] = None
    isBlocked: Optional[int] = None