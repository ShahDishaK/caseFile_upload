from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ClientModel(BaseModel):
    crNumber:int
    vatNumber:int
    vatPercentage:int
    isDeleted: Optional[bool] = False
    isBlocked: Optional[bool] = False
    
class UpdateClientRequest(BaseModel):
    crNumber:Optional[int]=None
    vatNumber:Optional[int]=None
    vatPercentage:Optional[int]=None
    lawyerId :Optional[int]=None
    isDeleted: Optional[bool] = None
    isBlocked: Optional[bool] = None