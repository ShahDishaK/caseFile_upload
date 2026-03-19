# Importing libraries
from sqlalchemy.orm import Session
from dtos.user_models import UpdateUserProfile, UserVerification,ForgotPassword
from dtos.auth_models import UserModel
from helper.api_helper import APIHelper
from models.users_table import User
from fastapi import HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


SECREAT_KEY='342e33d140d858d4eb74ae725b7d3a0fe4aa8dade3f6f435fae690b92b6f3001'
ALGORITHM='HS256'

bcrypt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

oauth2_bearer=OAuth2PasswordBearer(tokenUrl='/auth/login')

class UserController:
    def read_all(user: UserModel ,db: Session ):
        if user is None or user.role != 'admin':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        users = db.query(User).all()
        return users


    def get_user(user: UserModel,db: Session):
        if user is None:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        user = db.query(User).filter(User.id == user.id).first()
        return user

    def change_password(user_verification: UserVerification,user: UserModel,db: Session ):
        if user is None:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
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
                return APIHelper.send_not_found_error(errorMessageKey='translations.USER_NOT_FOUND')
        # Update password
        user_model.password = bcrypt_context.hash(user_verification.new_password)
        db.add(user_model)
        db.commit()

        return {"message": "Password changed successfully"}
    
    def update_profile(update_user_profile: UpdateUserProfile, user: UserModel, db: Session):
        if user is None:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        user_model = db.query(User).filter(User.id == user.id).first()

        update_data = update_user_profile.dict(exclude_unset=True, exclude_none=True)

        for key, value in update_data.items():
            setattr(user_model, key, value)
                
        db.commit()
        db.refresh(user_model)

        return user_model

