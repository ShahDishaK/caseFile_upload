from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserModel(BaseModel):
    id: str
    email: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class TokenModel(UserModel):
    access_token: str
    token_type: Optional[str] = 'Bearer'
