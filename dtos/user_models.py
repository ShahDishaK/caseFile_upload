from typing import Optional
from pydantic import BaseModel, Field, validator, constr
from dtos.auth_models import UserModel

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

class ForgotPassword(BaseModel):
    email:str
    new_password:str

class UpdateUserProfile(BaseModel):
    name: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phoneNumber: Optional[constr(regex="^[0-9]{10}$")] = None
    address: Optional[str] = None
