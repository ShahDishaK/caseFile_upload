from typing_extensions import Annotated
from fastapi import Depends, APIRouter, HTTPException,Request 
from pydantic import BaseModel
from models.users_table import User
from passlib.context import CryptContext
from config.db_config import dp_dependency
# from TodoApp.database import dp_dependency
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
from helper.token_helper import TokenHelper
from helper.api_helper import APIHelper

# from TodoApp.models import Users
# from fastapi.templating import Jinja2Templates
# from core.templates import templates
import os  

# router = APIRouter(
#     prefix='/auth',
#     tags=['auth']
# )
auth= APIRouter(prefix='/auth',tags=['Auth'])


# SECREAT_KEY = '508298e8120b8a33d8574c09bd98dde555f5329baffb27f467916a8edd8bf5dd'
# ALGORITHM = 'HS256'


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ ONLY THIS
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")


# templates = Jinja2Templates(directory="/TodoApp/templates")

### pages  ###
# @router.get("/login-page")
# def render_login_page(request:Request):
#     return templates.TemplateResponse("login.html",{"request":request})

# @router.get("/register-page")
# def render_register_page(request: Request):
#     return templates.TemplateResponse("register.html", {"request": request})



from dtos.auth_models import UserModel as CreateUserRequest
from dtos.auth_models import TokenModel 
from helper.validation_helper import ValidationHelper



@auth.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: dp_dependency):
    create_user_model = User(
        email=create_user_request.email,
        name=create_user_request.name,
       firstName=create_user_request.first_name,
       lastName=create_user_request.last_name,
        password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
    )
   
    db.add(create_user_model)
    db.commit()


# def authenticate_user(username: str, password: str, db):
#     user = db.query(User).filter(User.name == username).first()
#     print(user)
#     if user is None:
#         return False
#     print(bcrypt_context.verify(password, user.password))
#     if not bcrypt_context.verify(password, user.password):
#         return False
#     return user




@auth.post("/login", response_model=TokenModel)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: dp_dependency
):
    user = ValidationHelper.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
    token = TokenHelper.create_access_token({'sub':user.name,'id': user.id, 'role':user.role})
    return {'access_token': token, 'token_type': 'bearer'}