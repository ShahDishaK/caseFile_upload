from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserModel(BaseModel):
    name: str
    first_name: str
    last_name: str
    email: str
    password: str
    phoneNumber:str
    role: str
    address: Optional[str] = None
    companyId:int
    isDeleted: Optional[bool] = False
   

class TokenModel(BaseModel):
    access_token: str
    token_type: Optional[str] = 'Bearer'
