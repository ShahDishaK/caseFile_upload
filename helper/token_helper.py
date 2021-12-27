# Importing libraries
from jose import JWTError, jwt
from typing import Optional
from datetime import datetime, timedelta
from helper.api_helper import APIHelper
from schemas.token_model import TokenData
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import os

# JWT Configuration

"""Please generate a new JWT_SECRET `using openssl rand -hex 32` command and add it in the .env file"""

# Initializing the Hashing alogorith 
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#Initialize with the login api url
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

class TokenHelper:
    # Creates an access token
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=30)
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
            return encoded_jwt

    # Verifies if an access token has expired or not
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                return APIHelper.send_unauthorized_error()
            token_data = TokenData(email=email)
            return token_data.email
        except JWTError:
            return APIHelper.send_unauthorized_error()
        
    # Verifies current logged in user
    def get_current_user(token: str = Depends(oauth2_scheme)):
        return TokenHelper.verify_token(token)
