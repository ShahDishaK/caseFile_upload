from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserModel(BaseModel):
    name: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class TokenModel(BaseModel):
    access_token: str
    token_type: Optional[str] = 'Bearer'
