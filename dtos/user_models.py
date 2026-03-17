from typing import Optional
from pydantic import BaseModel, Field, validator
from dtos.auth_models import UserModel

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

class ForgotPassword(BaseModel):
    email:str
    new_password:str

class UpdateUserProfile(BaseModel):
    name:str
    firstName:str
    lastName:str
    phoneNumber:str
    address:str
    role :str
    companyId:int