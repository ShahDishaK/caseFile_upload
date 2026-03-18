# Importing libraries
from typing import Optional
from dtos.auth_models import UserModel
from models.staff_table import Staff
from models.clients_table import Clients
from models.lawyers_table import Lawyers
from helper.api_helper import APIHelper
from sqlalchemy.orm import Session
from fastapi import HTTPException
from dtos.client_models import ClientModel as CreateClientRequest, UpdateClientRequest


class ClientController:

    # ✅ CREATE CLIENT (LAWYER ONLY)
    def create_client(create_client_request: CreateClientRequest, user: UserModel, db: Session):

        if user is None or user.role != 'lawyer':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
        if lawyer is None:
            raise HTTPException(status_code=404, detail="Lawyer not found")

        if lawyer.isBlocked == b'\x01':
            raise HTTPException(status_code=403, detail="You are blocked")

        client = Clients(
            crNumber=create_client_request.crNumber,
            vatNumber=create_client_request.vatNumber,
            vatPercentage=create_client_request.vatPercentage,
            lawyerId=lawyer.id,
            isDeleted=0,
            isBlocked=b'\x00'  # not blocked initially
        )

        db.add(client)
        db.commit()
        db.refresh(client)
        return client

    # ✅ READ ALL CLIENTS
    def read_all(user: UserModel, db: Session):

        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        #  LAWYER
        if user.role == 'lawyer':
            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
            if lawyer is None:
                raise HTTPException(status_code=404, detail="Lawyer not found")

            if lawyer.isBlocked == b'\x01':
                raise HTTPException(status_code=403, detail="You are blocked")

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
                raise HTTPException(
                    status_code=403,
                    detail="No accessible clients (blocked or not assigned)"
                )

            return clients

    # ✅ UPDATE CLIENT
    def update_client(client_id: int, update_client_request: UpdateClientRequest, user: UserModel, db: Session):

        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        client = db.query(Clients).filter(Clients.id == client_id).first()
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")

        #  LAWYER
        if user.role == 'lawyer':
            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
            if lawyer is None:
                raise HTTPException(status_code=404, detail="Lawyer not found")
            if lawyer.isBlocked == b'\x01':
                raise HTTPException(status_code=403, detail="You are blocked")
            if client.lawyerId != lawyer.id:
                raise HTTPException(status_code=403, detail="Not authorized")

        #  STAFF
        else:
            staff = db.query(Staff).filter(
                Staff.user_id == user.id,
                Staff.lawyerId == client.lawyerId,
                Staff.isBlocked == b'\x00',
            ).first()
            if staff is None:
                raise HTTPException(
                    status_code=403,
                    detail="You are blocked or not assigned to this lawyer"
                )
            if client.isBlocked == b'\x01':
                raise HTTPException(
                    status_code=403,
                    detail="Client is blocked for this lawyer"
                )

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
            raise HTTPException(status_code=404, detail="Lawyer not found")
        if lawyer.isBlocked == b'\x01':
            raise HTTPException(status_code=403, detail="You are blocked")

        client = db.query(Clients).filter(Clients.id == client_id).first()
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")
        if client.lawyerId != lawyer.id:
            raise HTTPException(status_code=403, detail="Not authorized")

        client.isDeleted = 1
        db.commit()
        return {"message": "Client soft deleted successfully"}

    #  BLOCK CLIENT
    def block_client(client_id: int, user: UserModel, db: Session):

        if user is None or user.role != "lawyer":
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
        if lawyer is None:
            raise HTTPException(status_code=404, detail="Lawyer not found")
        if lawyer.isBlocked == b'\x01':
            raise HTTPException(status_code=403, detail="You are blocked")

        client = db.query(Clients).filter(Clients.id == client_id).first()
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")
        if client.lawyerId != lawyer.id:
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        client.isBlocked = b'\x01'
        db.commit()
        return {"message": "Client blocked successfully"}
