# Importing libraries
from dtos.auth_models import UserModel
from models.cases_table import Cases
from helper.api_helper import APIHelper
from models.lawyers_table import Lawyers
from models.courtSession_table import CourtSessions
from sqlalchemy.orm import Session
from fastapi import HTTPException
from dtos.courtsession_models import SessionModel as CreatSessionRequest

class CourtSessionController:

    def create_document(create_session_request: CreatSessionRequest,user: UserModel,db: Session ):
        if user is None:
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        if user.role!='lawyer':
            return APIHelper.send_forbidden_error(errorMessageKey='translations.FORBIDDEN')

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

    def read_all(user: UserModel, db: Session):

        if user is None:
            return APIHelper.send_unauthorized_error(
                errorMessageKey='translations.UNAUTHORIZED'
            )

        if user.role != 'lawyer':
            return APIHelper.send_forbidden_error(
                errorMessageKey='translations.FORBIDDEN'
            )

        lawyer = db.query(Lawyers).filter(
            Lawyers.userId == user.id
        ).first()

        if lawyer is None:
            return APIHelper.send_not_found_error(
                errorMessageKey='translations.LAWYER_NOT_FOUND'
            )

        if lawyer.isBlocked == 1:
            return APIHelper.send_forbidden_error(
                errorMessageKey='translations.BLOCKED'
            )

        sessions = db.query(CourtSessions, Cases).join(
            Cases, CourtSessions.caseId == Cases.id
        ).filter(
            CourtSessions.lawyerId == lawyer.id,
            Cases.isDeleted == 0
        ).all()
        return [
            {
                "session": session,
                "case": case
            }
            for session, case in sessions
        ]