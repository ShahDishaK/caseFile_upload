# Importing libraries
from typing import Optional
from dtos.auth_models import UserModel
from models.staff_table import Staff
from models.lawyers_table import Lawyers
from helper.api_helper import APIHelper
from models.cases_table import Cases
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
from dtos.case_models import CaseModel as CreateCaseRequest, UpdateCaseRequest
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models.cases_table import Cases, CaseStatus
from sqlalchemy import func



class CaseController:
    def create_case(create_case_request: CreateCaseRequest,user: UserModel,db: Session):
        if user is None or user.role != 'lawyer':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
        
        create_case_model = Cases(
            caseNumber=create_case_request.caseNumber,
        title = create_case_request.title,
        type=create_case_request.type,
        description =create_case_request.description,
        lawyerId=lawyer.id,
        caseStage=create_case_request.caseStage,
        caseCity=create_case_request.caseCity,
        status=create_case_request.status,
        caseClosedDate=create_case_request.caseClosedDate,
        clientId=create_case_request.clientId
        )
        db.add(create_case_model)
        db.commit()

  
    def read_all(user: UserModel, db: Session):

        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(
                errorMessageKey='translations.UNAUTHORIZED'
            )

        # LAWYER
        if user.role == 'lawyer':

            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

            if lawyer is None:
                raise HTTPException(status_code=404, detail="Lawyer not found")

            cases = db.query(Cases).filter(
                Cases.lawyerId == lawyer.id,
                Cases.isDeleted.is_(False)
            ).all()

            return cases

        # STAFF
        else:

            staff = db.query(Staff).filter(Staff.user_id == user.id).first()

            if staff is None:
                raise HTTPException(status_code=404, detail="Staff not found")

            cases = db.query(Cases).filter(
                Cases.id == staff.caseId,
                Cases.isDeleted.is_(False)
            ).all()

            return cases

    def update_case(case_id: int,update_case_request: UpdateCaseRequest,user: UserModel,db: Session ):
        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        case_model = db.query(Cases).filter(Cases.id == case_id).first()

        if case_model is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.UNAUTHORIZED')
        if user.role=='lawyer':
            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

            if lawyer is None:
                raise HTTPException(status_code=404, detail="Lawyer not found")

            if case_model.lawyerId==lawyer.id:
                update_data = update_case_request.dict(exclude_unset=True, exclude_none=True)

                for key, value in update_data.items():
                    setattr(case_model, key, value)
                
                db.commit()
                db.refresh(case_model)

                return case_model
            else:
                raise HTTPException(status_code=404, detail="Lawyer not found")

        else:
            staff = db.query(Staff).filter(Staff.user_id == user.id).first()
            if staff is None:
                raise HTTPException(status_code=404, detail="Staff not found")
            
            if case_model.id==staff.caseId:
                update_data = update_case_request.dict(exclude_unset=True, exclude_none=True)

                for key, value in update_data.items():
                    setattr(case_model, key, value)
                
                db.commit()
                db.refresh(case_model)

                return case_model


    def soft_delete_case(case_id: int, user: UserModel, db: Session):

        if user is None or user.role != "lawyer":
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
        case_model = db.query(Cases).filter(Cases.id == case_id).first()
    
        if lawyer is None:
            raise HTTPException(status_code=404, detail="Lawyer not found")

        if case_model.lawyerId==lawyer.id:
            db.query(Cases).filter(Cases.id == case_id).update(
                {"isDeleted": True}
            )

            db.commit()

            return {"message": "Case soft deleted successfully"}
        
