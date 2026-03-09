# # Importing libraries
# from dtos.auth_models import TokenModel
# from dtos.base_response_model import BaseResponseModel
# from helper.api_helper import APIHelper
# from helper.token_helper import TokenHelper
# from helper.hashing import Hash
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm


# class AuthController:
#     def login(request: OAuth2PasswordRequestForm) -> BaseResponseModel:
#         user = Hash.authenticate_user(
#             username=request.username, password=request.password)
#         access_token = TokenHelper.create_access_token(
#             data={"id": user.id}
#         )
#         response = TokenModel(access_token=access_token, **user.__dict__)
#         return APIHelper.send_success_response(data=response, successMessageKey='translations.LOGIN_SUCCESS')


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
from dtos.auth_models import UserModel as CreateUserRequest
from dtos.auth_models import TokenModel 
from helper.validation_helper import ValidationHelper



# from TodoApp.models import Users
# from fastapi.templating import Jinja2Templates
# from core.templates import templates
import os  

auth= APIRouter(prefix='/auth',tags=['Auth'])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

# templates = Jinja2Templates(directory="/TodoApp/templates")

### pages  ###
# @router.get("/login-page")
# def render_login_page(request:Request):
#     return templates.TemplateResponse("login.html",{"request":request})

# @router.get("/register-page")
# def render_register_page(request: Request):
#     return templates.TemplateResponse("register.html", {"request": request})



@auth.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: dp_dependency):
    create_user_model = User(
        name=create_user_request.name,
       firstName=create_user_request.first_name,
       lastName=create_user_request.last_name,
        email=create_user_request.email,
        password=bcrypt_context.hash(create_user_request.password),
        phoneNumber=create_user_request.phoneNumber,
        role=create_user_request.role,
        companyId=create_user_request.companyId,
        isDeleted=create_user_request.isDeleted
    )
    db.add(create_user_model)
    db.commit()


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