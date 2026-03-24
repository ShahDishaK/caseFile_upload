# Importing libraries
from dtos.auth_models import UserModel
from helper.api_helper import APIHelper
from models.lawyers_table import Lawyers
from models.courtSession_table import CourtSessions
from sqlalchemy.orm import Session
from fastapi import HTTPException
from dtos.courtsession_models import SessionModel as CreatSessionRequest
import os
import i18n

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
i18n.load_path.append(os.path.join(BASE_DIR, 'language'))
i18n.set('filename_format', '{namespace}.{locale}.{format}')
i18n.set('fallback', 'en')
i18n.set('locale', 'en')

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
        return create_session_model

    def read_all(user: UserModel ,db: Session ):
        if user is None or user.role !='lawyer':
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

        if lawyer is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')
        if lawyer.isBlocked == b'\x01':
            raise HTTPException(status_code=403, detail="You are blocked")

        # filter staff by lawyerId
        staff = db.query(CourtSessions).filter(
            CourtSessions.lawyerId == lawyer.id,
        ).all()

        return staff