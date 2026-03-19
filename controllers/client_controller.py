# Importing libraries
from dtos.auth_models import UserModel
from models.staff_table import Staff
from models.clients_table import Clients
from models.lawyers_table import Lawyers
from helper.api_helper import APIHelper
from sqlalchemy.orm import Session
from dtos.client_models import ClientModel as CreateClientRequest, UpdateClientRequest

class ClientController:

    def create_client(create_client_request: CreateClientRequest, user: UserModel, db: Session):

        if user is None or user.role != 'lawyer':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
        if lawyer is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')

        if lawyer.isBlocked == b'\x01':
            return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')

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

            clients = db.query(Clients).filter(
                Clients.lawyerId == lawyer.id,
                Clients.isDeleted == 0
            ).all()

            return clients

        #  STAFF
        else:
            clients = db.query(Clients).join(
                Staff, Staff.lawyerId == Clients.lawyerId
            ).filter(
                Staff.user_id == user.id,
                Staff.isBlocked == b'\x00',
                Clients.isDeleted == 0,
                Clients.isBlocked == b'\x00' 
            ).all()

            if not clients:
                return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED_OR_NOT_ASSINGED_CLIENT')


            return clients

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
                return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKEDCLIENT')


        # UPDATE LOGIC
        update_data = update_client_request.dict(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            setattr(client, key, value)

        db.commit()
        db.refresh(client)
        return client

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
