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


SECREAT_KEY='342e33d140d858d4eb74ae725b7d3a0fe4aa8dade3f6f435fae690b92b6f3001'
ALGORITHM='HS256'

bcrypt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

oauth2_bearer=OAuth2PasswordBearer(tokenUrl='/auth/login')

class UserController:
    def read_all(user: UserModel ,db: Session ):
        if user is None or user.role != 'admin':
            raise HTTPException(status_code=401,detail='Authentication Failed')
        users = db.query(User).all()
        return users


    def get_user(user: UserModel,db: Session):
        if user is None:
            raise HTTPException(status_code=401,detail='Authentication Failed')
        user = db.query(User).filter(User.id == user.id).first()
        return user

    def change_password(user_verification: UserVerification,user: UserModel,db: Session ):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
        user_model = db.query(User).filter(User.id == user.id).first()

        if not bcrypt_context.verify(user_verification.password, user_model.password):
            raise HTTPException(status_code=401, detail='Error on password change')
        user_model.password = bcrypt_context.hash(user_verification.new_password)
        db.add(user_model)
        db.commit()


    def forgot_password(user_verification: ForgotPassword, db: Session):
        
        user_model = db.query(User).filter(User.email == user_verification.email).first()

        # Check if the email matches
        if user_model is None:
            raise HTTPException(status_code=404, detail='User not found')
        # Update password
        user_model.password = bcrypt_context.hash(user_verification.new_password)
        db.add(user_model)
        db.commit()

        return {"message": "Password changed successfully"}

