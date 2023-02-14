from typing import Optional
from pydantic import BaseModel, validator
from dtos.auth_models import UserModel
from helper.validation_helper import ValidationHelper


class CreateUserModel(BaseModel):
    email: str
    password: str
    is_admin: Optional[bool] = 0
    _email = validator("email", allow_reuse=True)(
        ValidationHelper.is_valid_email)
    _password = validator("password", allow_reuse=True)(
        ValidationHelper.is_valid_email)