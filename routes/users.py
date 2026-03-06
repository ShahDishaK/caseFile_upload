# Importing libraries
from typing import Optional
from fastapi import APIRouter, Depends
# from config.constants import Constants
# from controllers.user_controller import UserController
# from dtos.user_models import CreateUserModel
# from helper.api_helper import APIHelper
# from helper.token_helper import TokenHelper

# Declaring router
# user = APIRouter(tags=['User'])

# Login API


# @user.post('/user')
# async def create_user(request: CreateUserModel = Depends(TokenHelper.get_current_user)):
#     return UserController.create_user(request)


# @user.get('/user')
# async def get_user(user: str = Depends(TokenHelper.get_current_user)):
#     return APIHelper.send_success_response(data=user, successMessageKey='translations.SUCCESS')


# @user.delete('/user/{user_id}')
# async def delete_user(user_id: int, _: str = Depends(TokenHelper.get_current_user)):
#     return UserController.delete_user(user_id)


# @user.get('/users')
# async def get_users(page: int, size: Optional[int] = Constants.PAGE_SIZE, _: str = Depends(TokenHelper.get_current_user)):
#     return UserController.get_users(page, size)


from fastapi import Depends
from sqlalchemy.orm import Session
from config.db_config import dp_dependency
from models.users_table import User

# @user.post("/users/")
# def create_user(username: str, email: str, db: Session = Depends(get_db)):
#     user = User(name=username, email=email)
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user

from typing_extensions import Annotated
from fastapi import APIRouter,Depends,HTTPException,Path
from starlette import status 
from helper.token_helper import TokenHelper
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from pydantic import BaseModel, Field

router=APIRouter(
    prefix='/users',
    tags=['users']
)
c=TokenHelper()

SECREAT_KEY='342e33d140d858d4eb74ae725b7d3a0fe4aa8dade3f6f435fae690b92b6f3001'
ALGORITHM='HS256'

bcrypt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

user_dependency=Annotated[dict,Depends(c.get_current_user)]

@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db:dp_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    users = db.query(User).all()
    return users

@router.put("/change_password",status_code=status.HTTP_200_OK)
async def change_password(user:user_dependency,db:dp_dependency,new_password:str,user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(User).filter(User.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
