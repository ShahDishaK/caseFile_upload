# Importing libraries
from dtos.auth_models import UserModel
from models.lawyers_table import Lawyers
from helper.api_helper import APIHelper
from models.staff_table import Staff
from models.blockedStaff_table import BlockedStaff
from sqlalchemy.orm import Session
from dtos.staff_models import StaffModel as CreateStaffRequest, UpdateStaffRequest


class StaffController:
    def create_staff(create_staff_request: CreateStaffRequest,user: UserModel,db: Session):
        if user is None or user.role !='lawyer':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        create_staff_model = Staff(
            user_id=create_staff_request.user_id,
            caseId=create_staff_request.caseId,
            lawyerId=create_staff_request.lawyerId,
            isBlocked=create_staff_request.isBlocked
        )
        db.add(create_staff_model)
        db.commit()

    def active_staff(db):
        return db.query(Staff).filter(Staff.isBlocked.is_(False))


    def read_all(user: UserModel, db: Session):
        if user is None or user.role != 'lawyer':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        # get lawyer using logged in user
        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

        if lawyer is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')
        if lawyer.isBlocked == b'\x01':
            return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')


        # filter staff by lawyerId
        staff = db.query(Staff).filter(
            Staff.lawyerId == lawyer.id,
            Staff.isBlocked==0
        ).all()

        return staff

    def update_staff(
        staff_id: int,
        update_staff_request: UpdateStaffRequest,
        user: UserModel,
    db: Session
    ):
        if user is None or user.role !='lawyer':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        staff_model = db.query(Staff).filter(Staff.id == staff_id).first()

        if staff_model is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.STAFF_NOT_FOUND')
        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

        if lawyer is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')
        if lawyer.isBlocked == b'\x01':
            return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')

        if Staff.lawyerId==lawyer.id:
            update_data = update_staff_request.dict(exclude_unset=True, exclude_none=True)

            for key, value in update_data.items():
                setattr(staff_model, key, value)
            
            db.commit()
            db.refresh(staff_model)

            return staff_model

    # delete the document
    def delete_staff(
        staff_id: int,
        user: UserModel ,
        db: Session
    ):
        if user is None or user.role !='lawyer':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        staff_model = db.query(Staff).filter(Staff.id == staff_id).first()
        if staff_model is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.STAFF_NOT_FOUND')
        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

        if lawyer is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')
        if lawyer.isBlocked == b'\x01':
            return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')

        if Staff.lawyerId==lawyer.id:
            Staff.delete(staff_model)
            db.commit()
            return {"message": "Document deleted successfully"}

    # Block staff
    def block_staff(client_id: int, user: UserModel, db: Session):

        if user is None or user.role != "lawyer":
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

        if lawyer is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')

        if lawyer.isBlocked == b'\x01':
            return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')

        staff = db.query(Staff).filter(Staff.id == client_id).first()

        if staff is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.STAFF_NOT_FOUND')

        if staff.lawyerId != lawyer.id:
            return APIHelper.send_forbidden_error(errorMessageKey='translations.NOT_ALLOWDED_TO_ACCESS_THIS_STAFF')

        staff.isBlocked = 1

        db.commit()
        db.refresh(staff)

        blocked_entry = BlockedStaff(
            lawyerId=lawyer.id,
            staffId=client_id,
        )

        db.add(blocked_entry)
        db.commit()

        return {"message": "Client blocked successfully"}