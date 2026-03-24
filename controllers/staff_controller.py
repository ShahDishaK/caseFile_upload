# Importing libraries
from dtos.auth_models import UserModel
from models.users_table import User
from models.lawyers_table import Lawyers
from helper.api_helper import APIHelper
from models.staff_table import Staff
from models.blockedStaff_table import BlockedStaff
from sqlalchemy.orm import Session
from dtos.staff_models import StaffModel as CreateStaffRequest, UpdateStaffRequest
import os
import i18n

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
i18n.load_path.append(os.path.join(BASE_DIR, 'language'))
i18n.set('filename_format', '{namespace}.{locale}.{format}')
i18n.set('fallback', 'en')
i18n.set('locale', 'en')


class StaffController:
    def create_staff(create_staff_request: CreateStaffRequest,user: UserModel,db: Session):
        if user is None or user.role !='lawyer':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        #  Step 1: Get existing user
        user_model = db.query(User).filter(User.id == create_staff_request.user_id).first()

        if user_model is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.USER_NOT_FOUND')
        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

        if lawyer is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')

        #  Step 2: Update user details
        user_model.name = create_staff_request.name
        user_model.firstName = create_staff_request.firstName
        user_model.lastName = create_staff_request.lastName
        user_model.phoneNumber = create_staff_request.phoneNumber
        user_model.address = create_staff_request.address
        user_model.gender = create_staff_request.gender
        user_model.role = 'staff'

        create_staff_model = Staff(
            user_id=create_staff_request.user_id,
            caseId=create_staff_request.caseId,
            lawyerId=lawyer.id,
        )
        db.add(create_staff_model)
        db.commit()
        return create_staff_model

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
        # staff = db.query(Staff).filter(
        #     Staff.lawyerId == lawyer.id,
        #     Staff.isBlocked==0
        # ).all()

        # return staff
        staff=db.query(Staff,User).join(
            User,Staff.user_id==User.id
        ).join(Lawyers,Staff.lawyerId==Lawyers.id).filter(Staff.lawyerId == lawyer.id,
            Staff.isBlocked==0).all()
        return [
            {
                "staff": staff,
                "user": user
            }
            for staff, user in staff    
        ]

    def update_staff(
        staff_id: int,
        update_staff_request: UpdateStaffRequest,
        user: UserModel,
    db: Session
    ):
        staff_model = db.query(Staff).filter(Staff.id == staff_id).first()

        if user is None or user.role !='lawyer' or staff_id.user_id!=user.id:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')


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
                if hasattr(staff_model, key):
                    setattr(staff_model, key, value)
            
            #  Update user fields
            user_model = db.query(User).filter(User.id == staff_model.userId).first()

            if user_model:
                if update_staff_request.name:
                    user_model.name = update_staff_request.name
                if update_staff_request.phoneNumber:
                    user_model.phoneNumber = update_staff_request.phoneNumber
                if update_staff_request.firstName:
                    user_model.firstName = update_staff_request.firstName
                if update_staff_request.lastName:
                    user_model.lastName = update_staff_request.lastName
                if update_staff_request.address:
                    user_model.address = update_staff_request.address
                if update_staff_request.gender:
                    user_model.gender = update_staff_request.gender
                # add more fields as needed

            db.commit()
            return {
                "lawyer": staff_model,
                "user": user_model
                }

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

        if staff_model.lawyerId==lawyer.id:
            db.delete(staff_model)
            db.commit()
            return {"message": "Document deleted successfully"}
        else:
            return APIHelper.send_forbidden_error(
                errorMessageKey='translations.NOT_ALLOWED_TO_DELETE_THIS_STAFF'
            )

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