# Importing libraries
from typing import Optional
from dtos.auth_models import UserModel
from helper.api_helper import APIHelper
# from models.cases_table import Cases
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
from dtos.caseStatusHistory_models import CaseStatusHistoryModel as CreateCaseRequest, UpdateCaseStatusHistoryRequest
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models.caseStatusHistory_table import CaseStatusHistories
from sqlalchemy import func



class CaseController:
    def create_case(create_case_request: CreateCaseRequest,user: UserModel,db: Session):
        if user is None or user.role != 'lawyer':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        create_case_model = CaseStatusHistories(
            caseId=create_case_request.caseId,
            title = create_case_request.title,
            type=create_case_request.type,
            description =create_case_request.description,
            caseStage=create_case_request.caseStage,
            caseCity=create_case_request.caseCity,
            status=create_case_request.status,
            caseClosedDate=create_case_request.caseClosedDate,
            clientId=create_case_request.clientId
        )
        db.add(create_case_model)
        db.commit()

    def active_cases(db):
        return db.query(CaseStatusHistories).filter(CaseStatusHistories.isDeleted.is_(False))

    def read_all(user: UserModel,db: Session ):
        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        cases = CaseController.active_cases(db).all()
        return cases


    def update_case(case_id: int,update_case_request: UpdateCaseStatusHistoryRequest,user: UserModel,db: Session ):
        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        case_model = db.query(CaseStatusHistories).filter(CaseStatusHistories.id == case_id).first()

        if case_model is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.UNAUTHORIZED')

        update_data = update_case_request.dict(exclude_unset=True, exclude_none=True)

        for key, value in update_data.items():
            setattr(case_model, key, value)
        
        db.commit()
        db.refresh(case_model)

        return case_model


    def delete_case(case_id: int, user: UserModel, db: Session):

        if user is None or user.role != "lawyer":
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        cases=db.query(CaseStatusHistories).filter(CaseStatusHistories.id == case_id)
        db.delete(cases)
        db.commit()

        return {"message": "CaseHistory deleted successfully"}
    
