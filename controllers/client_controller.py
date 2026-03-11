# Importing libraries
from typing import Optional
from helper.api_helper import APIHelper
from models.clients_table import Clients
from fastapi import APIRouter, Depends
from fastapi import Depends
from sqlalchemy.orm import Session
from config.db_config import dp_dependency
from typing_extensions import Annotated
from fastapi import APIRouter,Depends,HTTPException,Path
from starlette import status 
from helper.token_helper import TokenHelper
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from pydantic import BaseModel, Field
from dtos.client_models import ClientModel as CreateClientRequest, UpdateClientRequest

case=APIRouter(
    prefix='/client',
    tags=['client']
)

user_dependency=Annotated[dict,Depends(TokenHelper.get_current_user)]

@case.post("/client", status_code=status.HTTP_201_CREATED)
async def create_client(create_client_request: CreateClientRequest,user:user_dependency,db:dp_dependency):
    if user is None or user.role != 'lawyer':
        return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
    create_client_model = Clients(
        user_id=create_client_request.user_id,
        crNumber=create_client_request.crNumber,
        vatNumber=create_client_request.vatNumber,
        vatPercentage=create_client_request.vatPercentage,
        caseId=create_client_request.caseId,
        documentId=create_client_request.documentId
    )
    db.add(create_client_model)
    db.commit()
    
def active_cases(db):
    return db.query(Cases).filter(Cases.isDeleted.is_(False))
@case.get("/",status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db:dp_dependency):
    if user is None or user.role not in ['lawyer', 'staff']:
        return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
    cases = active_cases(db).all()
    return cases


@case.patch("/case/{case_id}", status_code=status.HTTP_200_OK)
async def update_case(case_id: int,update_case_request: UpdateCaseRequest,user: user_dependency,db: dp_dependency):
    if user is None or user.role not in ['lawyer', 'staff']:
        return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

    case_model = db.query(Cases).filter(Cases.id == case_id).first()

    if case_model is None:
        return APIHelper.send_not_found_error(errorMessageKey='translations.UNAUTHORIZED')

    update_data = update_case_request.dict(exclude_unset=True, exclude_none=True)

    for key, value in update_data.items():
        setattr(case_model, key, value)
    
    db.commit()
    db.refresh(case_model)

    return case_model


@case.delete("/{case_id}", status_code=status.HTTP_200_OK)
async def soft_delete_case(case_id: int, user: user_dependency, db: dp_dependency):

    if user is None or user.role != "lawyer":
        return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

    db.query(Cases).filter(Cases.id == case_id).update(
        {"isDeleted": True}
    )

    db.commit()

    return {"message": "Case soft deleted successfully"}