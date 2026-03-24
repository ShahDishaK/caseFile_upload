# Importing libraries
from dtos.auth_models import UserModel
from models.users_table import User
from helper.api_helper import APIHelper
from sqlalchemy.orm import Session
from models.lawyers_table import Lawyers
from dtos.lawyer_models import LawyerModel as CreateLawyerRequest, UpdateLawyerRequest
import os
import i18n
from sqlalchemy.exc import SQLAlchemyError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
i18n.load_path.append(os.path.join(BASE_DIR, 'language'))
i18n.set('filename_format', '{namespace}.{locale}.{format}')
i18n.set('fallback', 'en')
i18n.set('locale', 'en')


class LawyerController:

    def create_lawyer(create_lawyer_request: CreateLawyerRequest, user: UserModel, db: Session):

        if user is None or user.role != 'admin':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        #  Step 1: Get existing user
        user_model = db.query(User).filter(User.id == create_lawyer_request.userId).first()

        if user_model is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.USER_NOT_FOUND')
        try:
            #  Step 2: Update user details
            user_model.name = create_lawyer_request.name
            user_model.firstName = create_lawyer_request.firstName
            user_model.lastName = create_lawyer_request.lastName
            user_model.phoneNumber = create_lawyer_request.phoneNumber
            user_model.address = create_lawyer_request.address
            user_model.gender = create_lawyer_request.gender
            user_model.role = 'lawyer'

            # 🔹 Step 3: Create lawyer entry
            create_lawyer_model = Lawyers(
                userId=user_model.id,
                specialization=create_lawyer_request.specialization,
                isBlocked=create_lawyer_request.isBlocked
            )

            db.add(create_lawyer_model)
            db.commit()

            return APIHelper.send_success_response(successMessageKey='translations.SUCCESS')
        except SQLAlchemyError as e:
            db.rollback()  # VERY IMPORTANT
            return APIHelper.send_internal_server_error(
                errorMessageKey='translations.DB_ERROR'
            )

    def read_all(user: UserModel ,db: Session ):
        if user is None or user.role !="admin":
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
       
        lawyers = db.query(Lawyers, User).join(
                User, Lawyers.userId == User.id
            ).filter(
                Lawyers.isBlocked.is_(False),Lawyers.isDeleted.is_(False)
            ).all()

        return [
                {
                    "lawyer": lawyer,
                    "user": user
                }
                for lawyer, user in lawyers
            ]

    def update_lawyer(lawyer_id: int, update_lawyer_request: UpdateLawyerRequest, user: UserModel, db: Session):

        if user is None or user.role != 'admin':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        lawyer_model = db.query(Lawyers).filter(Lawyers.id == lawyer_id).first()

        if lawyer_model is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')

        # 🔹 Update lawyer fields
        update_data = update_lawyer_request.dict(exclude_unset=True, exclude_none=True)

        for key, value in update_data.items():
            if hasattr(lawyer_model, key):
                setattr(lawyer_model, key, value)

        #  Update user fields
        user_model = db.query(User).filter(User.id == lawyer_model.userId).first()

        if user_model:
            if update_lawyer_request.name:
                user_model.name = update_lawyer_request.name
            if update_lawyer_request.phoneNumber:
                user_model.phoneNumber = update_lawyer_request.phoneNumber
            if update_lawyer_request.firstName:
                user_model.firstName = update_lawyer_request.firstName
            if update_lawyer_request.lastName:
                user_model.lastName = update_lawyer_request.lastName
            if update_lawyer_request.address:
                user_model.address = update_lawyer_request.address
            if update_lawyer_request.gender:
                user_model.gender = update_lawyer_request.gender
            # add more fields as needed
        db.commit()
        return {
            "lawyer": lawyer_model,
            "user": user_model
            }


    def delete_lawyer(lawyer_id: int, user: UserModel, db: Session):

            print("DELETE API HIT FOR ID:", lawyer_id)

            if user is None or user.role != "admin":
                return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

            lawyer = db.query(Lawyers).filter(Lawyers.id == lawyer_id).first()
            print("LAWYER MODEL:", lawyer.isDeleted, lawyer.id)

            if lawyer is None:
                return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')

            lawyer.isDeleted = 1

            db.commit()
            db.refresh(lawyer)
            
            print("AFTER COMMIT:", lawyer.isDeleted)

            return APIHelper.send_success_response(successMessageKey='translations.SUCCESS')
    def block_lawyer(lawyer_id: int, user: UserModel,db: Session):

        if user is None or user.role != "admin":
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        db.query(Lawyers).filter(Lawyers.id == lawyer_id).update(
            {"isBlocked":1}
        )

        db.commit()

        return APIHelper.send_success_response(successMessageKey='translations.SUCCESS')
