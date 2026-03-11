from typing import Optional
from pydantic import BaseModel, Field, validator
from dtos.auth_models import UserModel

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)