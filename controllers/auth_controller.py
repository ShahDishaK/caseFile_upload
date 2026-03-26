from sqlalchemy.orm import Session
from models.users_table import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from helper.token_helper import TokenHelper
from helper.api_helper import APIHelper
from dtos.auth_models import UserModel as CreateUserRequest
from helper.validation_helper import ValidationHelper

# auth= APIRouter(prefix='/auth',tags=['Auth'])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

class AuthController:
    
    def login_for_access_token(
        form_data: OAuth2PasswordRequestForm ,
        db: Session
    ):
        user = ValidationHelper.authenticate_user(form_data.username, form_data.password, db)
        if not user:
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        token = TokenHelper.create_access_token({'sub':user.email,'id': user.id, 'role':user.role})
        return {'access_token': token, 'token_type': 'bearer'}