from sqlalchemy.orm import Session
from models.users_table import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from helper.token_helper import TokenHelper
from helper.api_helper import APIHelper
from dtos.auth_models import UserModel as CreateUserRequest
from helper.validation_helper import ValidationHelper
import os
import i18n

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
i18n.load_path.append(os.path.join(BASE_DIR, 'language'))
i18n.set('filename_format', '{namespace}.{locale}.{format}')
i18n.set('fallback', 'en')
i18n.set('locale', 'en')

# auth= APIRouter(prefix='/auth',tags=['Auth'])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

class AuthController:
    def create_user(create_user_request: CreateUserRequest, db: Session ):
        create_user_model = User(
            email=create_user_request.email,
            password=bcrypt_context.hash(create_user_request.password),
            companyId=create_user_request.companyId
        )
        db.add(create_user_model)
        db.commit()
        return {"UserId is":create_user_model.id}
    
    def login_for_access_token(
        form_data: OAuth2PasswordRequestForm ,
        db: Session
    ):
        user = ValidationHelper.authenticate_user(form_data.username, form_data.password, db)
        if not user:
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        token = TokenHelper.create_access_token({'sub':user.email,'id': user.id, 'role':user.role})
        return {'access_token': token, 'token_type': 'bearer'}