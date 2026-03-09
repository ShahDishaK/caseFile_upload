# Importing libraries
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dtos.auth_models import UserModel
from helper.api_helper import APIHelper
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
from config.db_config import dp_dependency
from utils.db_helper import DBHelper

# JWT Configuration
load_dotenv()
"""Please generate a new JWT_SECRET `using openssl rand -hex 32` command and add it in the .env file"""

# Initializing the Hashing alogorith
JWT_SECRET = os.getenv("JWT_SECRET")
print(JWT_SECRET)
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class TokenHelper:
    def create_access_token(data):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, JWT_SECRET, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(token: str, db: dp_dependency) -> UserModel:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
            user_id: int = payload.get("id")
            username: str = payload.get('sub')
            user_role: str = payload.get('role')
            if user_id is None:
                return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
                # return {"error":"404"}
        except JWTError:
                # return {"error":"404"}
            
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        user = DBHelper.get_user_by_id(user_id,db)
        if user is None:
            return APIHelper.send_unauthorized_error(
                errorMessageKey='translations.UNAUTHORIZED')
                # return {"error":"404"}

        return user

    def get_current_user(db: dp_dependency,token: str = Depends(oauth2_scheme)) -> UserModel:
        return TokenHelper.verify_token(token,db)
