# Importing libraries
from typing import Optional
from fastapi import APIRouter, Depends
from fastapi import Depends
from sqlalchemy.orm import Session
from config.db_config import dp_dependency, get_db
from dtos.user_models import UserVerification,ForgotPassword
from dtos.auth_models import UserModel
from models.users_table import User
from typing_extensions import Annotated
from fastapi import APIRouter,Depends,HTTPException,Path
from starlette import status 
from helper.token_helper import TokenHelper
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from pydantic import BaseModel, Field
from controllers.user_controller import UserController

router=APIRouter(
    prefix='/users',
    tags=['users']
)


SECREAT_KEY='342e33d140d858d4eb74ae725b7d3a0fe4aa8dade3f6f435fae690b92b6f3001'
ALGORITHM='HS256'

bcrypt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

oauth2_bearer=OAuth2PasswordBearer(tokenUrl='/auth/login')
user_dependency=Annotated[dict,Depends(TokenHelper.get_current_user)]

@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    return UserController.read_all(user,db)

@router.get("/profile",status_code=status.HTTP_200_OK)
async def get_user(user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    return UserController.get_user(user,db)

@router.put("/change_password",status_code=status.HTTP_200_OK)
async def change_password(user_verification: UserVerification,user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    return UserController.change_password(user_verification,user,db)

@router.put("/forgot_password", status_code=status.HTTP_200_OK)
async def forgot_password(user_verification: ForgotPassword, db: Session = Depends(get_db)):
    return UserController.forgot_password(user_verification,db)