# Importing libraries
from dtos.auth_models import UserModel
from models.staff_table import Staff
from models.lawyers_table import Lawyers
from models.cases_table import Cases
from helper.api_helper import APIHelper
from sqlalchemy.orm import Session

class CaseController:

    #  CREATE CASE
    def create_case(create_case_request, user: UserModel, db: Session):

        if user is None or user.role != 'lawyer':
            return APIHelper.send_unauthorized_error(
                errorMessageKey='translations.UNAUTHORIZED'
            )

        lawyer = db.query(Lawyers).filter(
            Lawyers.userId == user.id
        ).first()

        if not lawyer:
            return APIHelper.send_not_found_error(
                errorMessageKey='translations.LAWYER_NOT_FOUND'
            )

        #  BLOCK CHECK
        if lawyer.isBlocked == b'\x01':
            return APIHelper.send_forbidden_error(
                errorMessageKey='translations.BLOCKED'
            )

        case = Cases(
            caseNumber=create_case_request.caseNumber,
            title=create_case_request.title,
            type=create_case_request.type,
            description=create_case_request.description,
            lawyerId=lawyer.id,
            caseStage=create_case_request.caseStage,
            caseCity=create_case_request.caseCity,
            status=create_case_request.status,
            caseClosedDate=create_case_request.caseClosedDate,
            clientId=create_case_request.clientId,
            isDeleted=b'\x00'
        )

        db.add(case)
        db.commit()
        db.refresh(case)

        return case


    #  READ ALL CASES
    def read_all(user: UserModel, db: Session):

        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(
                errorMessageKey='translations.UNAUTHORIZED'
            )

        # ================= LAWYER =================
        if user.role == 'lawyer':

            lawyer = db.query(Lawyers).filter(
                Lawyers.userId == user.id,
                Lawyers.isDeleted == b'\x00'
            ).first()

            if not lawyer:
                return APIHelper.send_not_found_error(
                    errorMessageKey='translations.LAWYER_NOT_FOUND'
                )

            if lawyer.isBlocked == b'\x01':
                return APIHelper.send_forbidden_error(
                    errorMessageKey='translations.BLOCKED'
                )

            cases = db.query(Cases).filter(
                Cases.lawyerId == lawyer.id,
                Cases.isDeleted == b'\x00'
            ).all()

            return cases

        # ================= STAFF =================
        elif user.role == 'staff':

            staff_records = db.query(Staff).filter(
                Staff.user_id == user.id
            ).all()

            if not staff_records:
                return APIHelper.send_not_found_error(
                    errorMessageKey='translations.STAFF_NOT_FOUND'
                )

            allowed_case_ids = [
                staff.caseId
                for staff in staff_records
                if staff.isBlocked == b'\x00' and staff.caseId is not None
            ]

            if not allowed_case_ids:
                return APIHelper.send_forbidden_error(
                    errorMessageKey='translations.BLOCKED'
                )

            cases = db.query(Cases).filter(
                Cases.id.in_(allowed_case_ids),
                Cases.isDeleted == b'\x00'
            ).all()

            return cases


    #  UPDATE CASE
    def update_case(case_id: int, update_case_request, user: UserModel, db: Session):

        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(
                errorMessageKey='translations.UNAUTHORIZED'
            )

        case = db.query(Cases).filter(
            Cases.id == case_id,
            Cases.isDeleted == b'\x00'
        ).first()

        if not case:
            return APIHelper.send_not_found_error(
                errorMessageKey='translations.CASE_NOT_FOUND'
            )

        # ================= LAWYER =================
        if user.role == 'lawyer':

            lawyer = db.query(Lawyers).filter(
                Lawyers.userId == user.id,
                Lawyers.isDeleted == b'\x00'
            ).first()

            if not lawyer:
                return APIHelper.send_not_found_error(
                    errorMessageKey='translations.LAWYER_NOT_FOUND'
                )

            if lawyer.isBlocked == b'\x01':
                return APIHelper.send_forbidden_error(
                    errorMessageKey='translations.BLOCKED'
                )

            if case.lawyerId != lawyer.id:
                return APIHelper.send_forbidden_error(
                    errorMessageKey='translations.NOT_ALLOWED'
                )

        # ================= STAFF =================
        elif user.role == 'staff':

            allowed = db.query(Cases).join(
                Staff, Cases.id == Staff.caseId
            ).filter(
                Cases.id == case_id,
                Staff.user_id == user.id,
                Staff.isBlocked == b'\x00'
            ).first()

            if not allowed:
                return APIHelper.send_unauthorized_error(
                    errorMessageKey='translations.UNAUTHORIZED'
                )

        #  UPDATE DATA
        update_data = update_case_request.dict(
            exclude_unset=True,
            exclude_none=True
        )

        for key, value in update_data.items():
            setattr(case, key, value)

        db.commit()
        db.refresh(case)

        return case


    #  SOFT DELETE
    def soft_delete_case(case_id: int, user: UserModel, db: Session):

        if user is None or user.role != "lawyer":
            return APIHelper.send_unauthorized_error(
                errorMessageKey='translations.UNAUTHORIZED'
            )

        lawyer = db.query(Lawyers).filter(
            Lawyers.userId == user.id
        ).first()

        if not lawyer:
            return APIHelper.send_not_found_error(
                errorMessageKey='translations.LAWYER_NOT_FOUND'
            )

        if lawyer.isBlocked == b'\x01':
            return APIHelper.send_forbidden_error(
                errorMessageKey='translations.BLOCKED'
            )

        case = db.query(Cases).filter(
            Cases.id == case_id,
            Cases.isDeleted == b'\x00'
        ).first()

        if not case:
            return APIHelper.send_not_found_error(
                errorMessageKey='translations.CASE_NOT_FOUND'
            )

        if case.lawyerId != lawyer.id:
            return APIHelper.send_forbidden_error(
                errorMessageKey='translations.NOT_ALLOWED'
            )

        case.isDeleted = b'\x01'

        db.commit()
        db.refresh(case)

        return {"message": "Case soft deleted successfully"}