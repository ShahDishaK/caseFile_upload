from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    lawyer = "lawyer"
    admin = "admin"
    staff = "staff"
    client="client"

class UserModel(BaseModel):
    name: str
    first_name:str
    last_name:str
    email: EmailStr
    phoneNumber: Optional[constr(regex="^[0-9]{10}$")]
    password: str
    role: str
    gender:str

    @validator("role")
    def convert_role_to_lowercase(cls, value):
        if value:
            return value.lower()
        return value
    address: Optional[str] = None
    companyId:int
    
class TokenModel(BaseModel):
    access_token: str
    token_type: Optional[str] = 'Bearer'
