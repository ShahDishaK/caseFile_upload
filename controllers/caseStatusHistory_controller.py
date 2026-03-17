# Importing libraries
from typing import Optional
from dtos.auth_models import UserModel
from models.lawyers_table import Lawyers
from models.cases_table import Cases
from models.staff_table import Staff
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
            oldStatus = create_case_request.oldStatus,
            newStatus=create_case_request.newStatus,
            
        )
        db.add(create_case_model)
        db.commit()

   
    def read_all(user: UserModel, db: Session):

        if user is None or user.role not in ['lawyer', 'staff']:
            raise HTTPException(status_code=401, detail="Authentication Failed")

        # LAWYER
        if user.role == 'lawyer':

            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

            if lawyer is None:
                raise HTTPException(status_code=404, detail="Lawyer not found")

            histories = db.query(CaseStatusHistories).join(
                Cases, CaseStatusHistories.caseId == Cases.id
            ).filter(
                Cases.lawyerId == lawyer.id
            ).all()

            return histories

        # STAFF
        else:

            staff = db.query(Staff).filter(Staff.user_id == user.id).first()

            if staff is None:
                raise HTTPException(status_code=404, detail="Staff not found")

            histories = db.query(CaseStatusHistories).filter(
                CaseStatusHistories.caseId == staff.caseId
            ).all()

            return histories


    def update_case(
    history_id: int,
    update_request: UpdateCaseStatusHistoryRequest,
    user: UserModel,
    db: Session
):

        # 🔒 Authentication check
        if user is None or user.role not in ['lawyer', 'staff']:
            raise HTTPException(status_code=401, detail="Authentication Failed")

        # =========================
        # 👨‍⚖️ LAWYER FLOW
        # =========================
        if user.role == 'lawyer':

            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

            if lawyer is None:
                raise HTTPException(status_code=404, detail="Lawyer not found")

            # 🔒 Secure query (VERY IMPORTANT)
            history = db.query(CaseStatusHistories).join(
                Cases, CaseStatusHistories.caseId == Cases.id
            ).filter(
                CaseStatusHistories.id == history_id,
                Cases.lawyerId == lawyer.id
            ).first()

            if history is None:
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized to update this history"
                )

        # =========================
        # 👨‍💼 STAFF FLOW
        # =========================
        else:

            staff = db.query(Staff).filter(Staff.user_id == user.id).first()

            if staff is None:
                raise HTTPException(status_code=404, detail="Staff not found")

            # 🔒 Secure query for staff
            history = db.query(CaseStatusHistories).join(
                Cases, CaseStatusHistories.caseId == Cases.id
            ).filter(
                CaseStatusHistories.id == history_id,
                Cases.id == staff.caseId
            ).first()

            if history is None:
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized to update this history"
                )

        # =========================
        # ✏️ UPDATE DATA
        # =========================
        update_data = update_request.dict(exclude_unset=True, exclude_none=True)

        for key, value in update_data.items():
            setattr(history, key, value)

        db.commit()
        db.refresh(history)

        return history
    def delete_case(case_history_id: int, user: UserModel, db: Session):

        if user is None or user.role != 'lawyer':
            raise HTTPException(status_code=401, detail="Authentication Failed")

        # get lawyer
        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

        if lawyer is None:
            raise HTTPException(status_code=404, detail="Lawyer not found")

        # get history
        history = db.query(CaseStatusHistories).filter(
            CaseStatusHistories.id == case_history_id
        ).first()

        if history is None:
            raise HTTPException(status_code=404, detail="History not found")

        # get case
        case = db.query(Cases).filter(Cases.id == history.caseId).first()

        if case is None:
            raise HTTPException(status_code=404, detail="Case not found")

        # authorization check
        if case.lawyerId != lawyer.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this history")

        # delete
        db.delete(history)
        db.commit()

        return {"message": "Case history deleted successfully"}