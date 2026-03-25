# Importing libraries
from dtos.auth_models import UserModel
from models.users_table import User
from models.staff_table import Staff
from models.clients_table import Clients
from models.lawyers_table import Lawyers
from helper.api_helper import APIHelper
from sqlalchemy.orm import Session
from dtos.client_models import ClientModel as CreateClientRequest, UpdateClientRequest

class ClientController:

    def create_client(create_client_request: CreateClientRequest, user: UserModel, db: Session):
        print(user.role)
        if user is None or user.role != 'lawyer':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
        if lawyer is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')

        if lawyer.isBlocked == b'\x01':
            return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')
        #  Step 1: Get existing user
        user_model = db.query(User).filter(User.id == create_client_request.userId).first()

        if user_model is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.USER_NOT_FOUND')

        #  Step 2: Update user details
        user_model.name = create_client_request.name
        user_model.firstName = create_client_request.firstName
        user_model.lastName = create_client_request.lastName
        user_model.phoneNumber = create_client_request.phoneNumber
        user_model.address = create_client_request.address
        user_model.gender = create_client_request.gender
        user_model.role = 'client'

        client = Clients(
            crNumber=create_client_request.crNumber,
            vatNumber=create_client_request.vatNumber,
            vatPercentage=create_client_request.vatPercentage,
            occupation=create_client_request.occupation,
            lawyerId=lawyer.id,
            userId=create_client_request.userId,
            isDeleted=0,
            isBlocked=b'\x00'  # not blocked initially
        )

        db.add(client)
        db.commit()
        db.refresh(client)
        return client

    def read_all(user: UserModel, db: Session):

        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        #  LAWYER
        if user.role == 'lawyer':
            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
            if lawyer is None:
                return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')

            if lawyer.isBlocked == b'\x01':
                return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')


            clients = db.query(Clients, User).join(
                User, Clients.userId == User.id
            ).filter(
                Clients.lawyerId == lawyer.id,
                Clients.isDeleted == 0,
            ).all()

            return [
                {
                    "client": client,
                    "user": user
                }
                for client, user in clients
            ]

        #  STAFF
        else:
            clients = db.query(Clients, User).join(
                User, Clients.userId == User.id
            ).join(
                Staff, Staff.lawyerId == Clients.lawyerId
            ).filter(
                Staff.user_id == user.id,
                Staff.isBlocked == b'\x00',
                Clients.isDeleted == 0,
                Clients.isBlocked == b'\x00'
            ).all()

            if not clients:
                return APIHelper.send_forbidden_error(
                    errorMessageKey='translations.BLOCKED_OR_NOT_ASSINGED_CLIENT'
                )

            return [
                {
                    "client": client,
                    "user": user
                }
                for client, user in clients
            ]

    #  UPDATE CLIENT
    def update_client(client_id: int, update_client_request: UpdateClientRequest, user: UserModel, db: Session):

        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        client = db.query(Clients).filter(Clients.id == client_id).first()
        if client is None:
                return APIHelper.send_not_found_error(errorMessageKey='translations.CLIENT_NOT_FOUND')

        #  LAWYER
        if user.role == 'lawyer':
            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
            if lawyer is None:
                return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')
            if lawyer.isBlocked == b'\x01':
                return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')
            if client.lawyerId != lawyer.id:
                return APIHelper.send_forbidden_error(errorMessageKey='translations.NOT_ALLOWDED_TO_ACCESS_THIS_CLIENT')

        #  STAFF
        else:
            staff = db.query(Staff).filter(
                Staff.user_id == user.id,
                Staff.lawyerId == client.lawyerId,
                Staff.isBlocked == b'\x00',
            ).first()
            if staff is None:
                return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED_OR_NOT_ASSIGNED_TO_LAWYER')
                
            if client.isBlocked == b'\x01':
                return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')


        # UPDATE LOGIC
        update_data = update_client_request.dict(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            setattr(client, key, value)
        #  Update user fields
        user_model = db.query(User).filter(User.id == client.userId).first()

        if user_model:
            if update_client_request.name:
                user_model.name = update_client_request.name
            if update_client_request.phoneNumber:
                user_model.phoneNumber = update_client_request.phoneNumber
            if update_client_request.firstName:
                user_model.firstName = update_client_request.firstName
            if update_client_request.lastName:
                user_model.lastName = update_client_request.lastName
            if update_client_request.address:
                user_model.address = update_client_request.address
            if update_client_request.gender:
                user_model.gender = update_client_request.gender
            # add more fields as needed

            db.commit()
            return {
                "lawyer": client,
                "user": user_model
                }


    #  SOFT DELETE CLIENT
    def soft_delete_client(client_id: int, user: UserModel, db: Session):

        if user is None or user.role != "lawyer":
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
        if lawyer is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')
        if lawyer.isBlocked == b'\x01':
            return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')

        client = db.query(Clients).filter(Clients.id == client_id).first()
        if client is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.CLIENT_NOT_FOUND')
        if client.lawyerId != lawyer.id:
            return APIHelper.send_forbidden_error(errorMessageKey='translations.NOT_ALLOWDED_TO_ACCESS_THIS_CLIENT')

        client.isDeleted = 1
        db.commit()
        return {"message": "Client soft deleted successfully"}

    #  BLOCK CLIENT
    def block_client(client_id: int, user: UserModel, db: Session):

        if user is None or user.role != "lawyer":
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
        if lawyer is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')
        if lawyer.isBlocked == b'\x01':
             return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')

        client = db.query(Clients).filter(Clients.id == client_id).first()
        if client is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.CLIENT_NOT_FOUND')
        if client.lawyerId != lawyer.id:
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        client.isBlocked = b'\x01'
        db.commit()
        return {"message": "Client blocked successfully"}
