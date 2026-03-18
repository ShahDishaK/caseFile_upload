# Importing libraries
from typing import Optional
from dtos.auth_models import UserModel
from helper.api_helper import APIHelper
from models.lawyers_table import Lawyers
from models.courtSession_table import CourtSessions
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
from dtos.courtsession_models import SessionModel as CreatSessionRequest




class CourtSessionController:

    def create_document(create_session_request: CreatSessionRequest,user: UserModel,db: Session ):
        if user is None or user.role !='lawyer':
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
        
        create_session_model = CourtSessions(
            sessionDate=create_session_request.sessionDate,
            sessionTime=create_session_request.sessionTime,
            courtName=create_session_request.courtName,
            caseId=create_session_request.caseId,
            lawyerId=lawyer.id,
            clientId=create_session_request.clientId,
        )
        db.add(create_session_model)
        db.commit()

    def read_all(user: UserModel ,db: Session ):
        if user is None or user.role !='lawyer':
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

        if lawyer is None:
            raise HTTPException(status_code=404, detail="Lawyer not found")
        if lawyer.isBlocked == b'\x01':
            raise HTTPException(status_code=403, detail="You are blocked")

        # filter staff by lawyerId
        staff = db.query(CourtSessions).filter(
            CourtSessions.lawyerId == lawyer.id,
        ).all()

        return staff