from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from passlib.context import CryptContext
from config.db_config import  get_db
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from dtos.auth_models import UserModel as CreateUserRequest
from controllers.auth_controller import AuthController

auth= APIRouter(prefix='/auth',tags=['Auth'])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

@auth.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: Session = Depends(get_db)):
    return AuthController.create_user(create_user_request,db)

@auth.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return AuthController.login_for_access_token(form_data,db)