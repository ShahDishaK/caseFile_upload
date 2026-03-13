# Importing libraries
from typing import Optional
from dtos.auth_models import UserModel
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
            raise HTTPException(status_code=401,detail='Authentication Failed')
        create_session_model = CourtSessions(
            sessionDate=create_session_request.sessionDate,
            sessionTime=create_session_request.sessionTime,
            courtName=create_session_request.courtName,
            caseId=create_session_request.caseId,
            lawyerId=create_session_request.lawyerId,
            clientId=create_session_request.clientId,
        )
        db.add(create_session_model)
        db.commit()

    def read_all(user: UserModel ,db: Session ):
        if user is None or user.role !='lawyer':
            raise HTTPException(status_code=401,detail='Authentication Failed')
        sessions = db.query(CourtSessions).all()
        return sessions