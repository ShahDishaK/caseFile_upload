from sqlalchemy.orm import Session
from typing_extensions import Annotated
from fastapi import Depends, APIRouter, HTTPException,Request 
from pydantic import BaseModel
from models.users_table import User
from passlib.context import CryptContext
from config.db_config import dp_dependency, get_db
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
from helper.token_helper import TokenHelper
from helper.api_helper import APIHelper
from dtos.auth_models import UserModel as CreateUserRequest
from dtos.auth_models import TokenModel 
from helper.validation_helper import ValidationHelper
import os  

# auth= APIRouter(prefix='/auth',tags=['Auth'])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

class AuthController:
    def create_user(create_user_request: CreateUserRequest, db: Session ):
        create_user_model = User(
            name=create_user_request.name,
        firstName=create_user_request.first_name,
        lastName=create_user_request.last_name,
            email=create_user_request.email,
            password=bcrypt_context.hash(create_user_request.password),
            phoneNumber=create_user_request.phoneNumber,
            role=create_user_request.role,
            address=create_user_request.address,
            companyId=create_user_request.companyId,
            isDeleted=create_user_request.isDeleted,
            isBlocked=create_user_request.isBlocked

        )
        db.add(create_user_model)
        db.commit()



    def login_for_access_token(
        form_data: OAuth2PasswordRequestForm ,
        db: Session
    ):
        user = ValidationHelper.authenticate_user(form_data.username, form_data.password, db)
        if not user:
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        token = TokenHelper.create_access_token({'sub':user.name,'id': user.id, 'role':user.role})
        return {'access_token': token, 'token_type': 'bearer'}