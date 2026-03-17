# Importing libraries
from typing import Optional
from dtos.auth_models import UserModel
from helper.api_helper import APIHelper
from fastapi import APIRouter, Depends
from fastapi import Depends
from sqlalchemy.orm import Session
from config.db_config import dp_dependency, get_db
from typing_extensions import Annotated
from fastapi import APIRouter,Depends,HTTPException,Path
from starlette import status 
from helper.token_helper import TokenHelper
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from pydantic import BaseModel, Field
from models.lawyers_table import Lawyers
from dtos.lawyer_models import LawyerModel as CreateLawyerRequest, UpdateLawyerRequest



class LawyerController:

    def create_lawyer(create_lawyer_request: CreateLawyerRequest,user: UserModel ,db: Session ):
        if user is None or user.role != 'admin':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        
        create_lawyer_model = Lawyers(
            userId=create_lawyer_request.userId,
            specialization=create_lawyer_request.specialization,
            isBlocked=create_lawyer_request.isBlocked
        )
        db.add(create_lawyer_model)
        db.commit()
  
    def active_lawyers(db):
        return db.query(Lawyers).filter(Lawyers.isBlocked.is_(False))


    def read_all(user: UserModel ,db: Session ):
        if user is None or user.role !="admin":
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        lawyers = LawyerController.active_lawyers(db).all()
        return lawyers

    def update_lawyer(lawyer_id: int,update_lawyer_request: UpdateLawyerRequest,user: UserModel,db: Session):
        if user is None or user.role !='admin':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        lawyer_model = db.query(Lawyers).filter(Lawyers.id == lawyer_id).first()

        if lawyer_model is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.UNAUTHORIZED')

        update_data = update_lawyer_request.dict(exclude_unset=True, exclude_none=True)

        for key, value in update_data.items():
            setattr(lawyer_model, key, value)
        
        db.commit()
        db.refresh(lawyer_model)

        return lawyer_model


    def delete_lawyer(lawyer_id: int, user: UserModel,db: Session ):

        if user is None or user.role != "admin":
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        lawyer=db.query(Lawyers).filter(Lawyers.id == lawyer_id).first()
        db.delete(lawyer)
        db.commit()

        return {"message": "Lawyer deleted successfully"}

    def block_lawyer(lawyer_id: int, user: UserModel,db: Session):

        if user is None or user.role != "admin":
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        db.query(Lawyers).filter(Lawyers.id == lawyer_id).update(
            {"isBlocked": True}
        )

        db.commit()

        return {"message": "Client blocked successfully"}