from dtos.auth_models import UserModel
from models.lawyers_table import Lawyers
from models.cases_table import Cases
from models.staff_table import Staff
from models.caseStatusHistory_table import CaseStatusHistories
from helper.api_helper import APIHelper
from sqlalchemy.orm import Session
from dtos.caseStatusHistory_models import CaseStatusHistoryModel as CreateCaseRequest, UpdateCaseStatusHistoryRequest

class CaseController:

    #  CREATE
    def create_case(create_case_request: CreateCaseRequest, user: UserModel, db: Session):

        if user is None or user.role != 'lawyer':
            return APIHelper.send_unauthorized_error(
                errorMessageKey='translations.UNAUTHORIZED'
            )

        lawyer = db.query(Lawyers).filter(
            Lawyers.userId == user.id
        ).first()

        if not lawyer:
            return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')

        #  FIXED BLOCK CHECK
        if lawyer.isBlocked == b'\x01':
            return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')
        new_history = CaseStatusHistories(
            caseId=create_case_request.caseId,
            oldStatus=create_case_request.oldStatus,
            newStatus=create_case_request.newStatus,
        )

        db.add(new_history)
        db.commit()
        db.refresh(new_history)

        return new_history


    #  READ ALL
    def read_all(user: UserModel, db: Session):

        if user is None or user.role not in ['lawyer', 'staff']:
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        # ================= LAWYER =================
        if user.role == 'lawyer':

            lawyer = db.query(Lawyers).filter(
                Lawyers.userId == user.id
            ).first()

            if not lawyer:
                return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')

            if lawyer.isBlocked == b'\x01':
                return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')

            histories = db.query(CaseStatusHistories).join(
                Cases, CaseStatusHistories.caseId == Cases.id
            ).filter(
                Cases.lawyerId == lawyer.id
            ).all()

            return histories

        # ================= STAFF =================
        else:

            histories = db.query(CaseStatusHistories).join(
                Cases, CaseStatusHistories.caseId == Cases.id
            ).join(
                Staff, Staff.caseId == Cases.id
            ).filter(
                Staff.user_id == user.id,
                Staff.isBlocked == b'\x00'   
            ).all()

            if not histories:
                return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED_OR_NOT_ASSIGENED_TO_HISTORY')


            return histories


    #  UPDATE
    def update_case(
        history_id: int,
        update_request: UpdateCaseStatusHistoryRequest,
        user: UserModel,
        db: Session
    ):

        if user is None or user.role not in ['lawyer', 'staff']:
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        # ================= LAWYER =================
        if user.role == 'lawyer':

            lawyer = db.query(Lawyers).filter(
                Lawyers.userId == user.id
            ).first()

            if not lawyer:
                return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')
            if lawyer.isBlocked == b'\x01':
                return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')

            history = db.query(CaseStatusHistories).join(
                Cases, CaseStatusHistories.caseId == Cases.id
            ).filter(
                CaseStatusHistories.id == history_id,
                Cases.lawyerId == lawyer.id
            ).first()

            if not history:
                APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')


        # ================= STAFF =================
        else:

            history = db.query(CaseStatusHistories).join(
                Cases, CaseStatusHistories.caseId == Cases.id
            ).join(
                Staff, Staff.caseId == Cases.id
            ).filter(
                CaseStatusHistories.id == history_id,
                Staff.user_id == user.id,
                Staff.isBlocked == b'\x00'   
            ).first()

            if not history:
                APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')


        #  UPDATE DATA
        update_data = update_request.dict(
            exclude_unset=True,
            exclude_none=True
        )

        for key, value in update_data.items():
            setattr(history, key, value)

        db.commit()
        db.refresh(history)

        return history


    #  DELETE
    def delete_case(case_history_id: int, user: UserModel, db: Session):

        if user is None or user.role != 'lawyer':
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        lawyer = db.query(Lawyers).filter(
            Lawyers.userId == user.id
        ).first()

        if not lawyer:
            return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')

        if lawyer.isBlocked == b'\x01':
            return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')

        history = db.query(CaseStatusHistories).filter(
            CaseStatusHistories.id == case_history_id
        ).first()

        if not history:
            return APIHelper.send_not_found_error(errorMessageKey='translations.HISTORY_NOT_FOUND')

        case = db.query(Cases).filter(
            Cases.id == history.caseId
        ).first()

        if not case:
            return APIHelper.send_not_found_error(errorMessageKey='translations.CASE_NOT_FOUND')

        if case.lawyerId != lawyer.id:
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')


        db.delete(history)
        db.commit()

        return {"message": "Case history deleted successfully"}