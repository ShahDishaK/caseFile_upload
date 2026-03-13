# Importing libraries
from typing import Optional
from dtos.auth_models import UserModel
from helper.api_helper import APIHelper
from models.clients_table import Clients
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
from dtos.client_models import ClientModel as CreateClientRequest, UpdateClientRequest



class ClientController:

    def create_client(create_client_request: CreateClientRequest,user: UserModel ,db: Session ):
        if user is None or user.role != 'lawyer':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        
        # Get lawyer using logged-in user's id
        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

        if lawyer is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')

        
        create_client_model = Clients(
            crNumber=create_client_request.crNumber,
            vatNumber=create_client_request.vatNumber,
            vatPercentage=create_client_request.vatPercentage,
            lawyerId=lawyer.id,
            isDeleted=create_client_request.isDeleted,
            isBlocked=create_client_request.isBlocked
        )
        db.add(create_client_model)
        db.commit()
  
    def active_clients(db):
        return db.query(Clients).filter(Clients.isDeleted.is_(False),Clients.isBlocked.is_(False))


    def read_all(user: UserModel ,db: Session ):
        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        cases = ClientController.active_clients(db).all()
        return cases

    def update_client(client_id: int,update_client_request: UpdateClientRequest,user: UserModel,db: Session):
        if user is None or user.role !='lawyer':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        case_model = db.query(Clients).filter(Clients.id == client_id).first()

        if case_model is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.UNAUTHORIZED')

        update_data = update_client_request.dict(exclude_unset=True, exclude_none=True)

        for key, value in update_data.items():
            setattr(case_model, key, value)
        
        db.commit()
        db.refresh(case_model)

        return case_model


    def soft_delete_client(client_id: int, user: UserModel,db: Session ):

        if user is None or user.role != "lawyer":
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        db.query(Clients).filter(Clients.id == client_id).update(
            {"isDeleted": True}
        )

        db.commit()

        return {"message": "Client soft deleted successfully"}

    def block_client(client_id: int, user: UserModel,db: Session):

        if user is None or user.role != "lawyer":
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        db.query(Clients).filter(Clients.id == client_id).update(
            {"isBlocked": True}
        )

        db.commit()

        return {"message": "Client blocked successfully"}