# Importing libraries
from dtos.auth_models import UserModel
from models.users_table import User
from models.staff_table import Staff
from models.clients_table import Clients
from models.lawyers_table import Lawyers
from helper.api_helper import APIHelper
from sqlalchemy.orm import Session
from dtos.client_models import ClientModel as CreateClientRequest, UpdateClientRequest
from helper.hashing import Hash
from models.cases_table import Cases
from models.documents_table import Documents
from models.tasks_table import Tasks
from models.caseStatusHistory_table import CaseStatusHistories
from models.courtSession_table import CourtSessions
from models.invoices_table import Invoices


class ClientController:

    def create_client(create_client_request: CreateClientRequest, user: UserModel, db: Session):
        print(user.role)
        if user is None:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        if user.role!='lawyer':
            return APIHelper.send_forbidden_error(errorMessageKey='translations.FORBIDDEN')

        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
        if lawyer is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')

        if lawyer.isBlocked == 1:
            return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')
        
        #  Step 2: Update user details
        user_model = User(
                name=create_client_request.name,
                firstName=create_client_request.firstName,
                lastName=create_client_request.lastName,
                phoneNumber=create_client_request.phoneNumber,
                address=create_client_request.address,
                gender=create_client_request.gender,
                email=create_client_request.email,
                password=Hash.get_hash(create_client_request.password),
                companyId=create_client_request.companyId,
                role='client'
            )

        db.add(user_model)
        db.commit()        
        db.refresh(user_model)  

        client = Clients(
            crNumber=create_client_request.crNumber,
            vatNumber=create_client_request.vatNumber,
            vatPercentage=create_client_request.vatPercentage,
            occupation=create_client_request.occupation,
            lawyerId=lawyer.id,
            userId=user_model.id,
        )

        db.add(client)
        db.commit()
        db.refresh(client)
        return client

    def read_all(user: UserModel, db: Session):

        if user is None :
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        if user.role not in ['lawyer','staff']:
            return APIHelper.send_forbidden_error(errorMessageKey='translations.FORBIDDEN')

        #  LAWYER
        if user.role == 'lawyer':
            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
            if lawyer is None:
                return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')

            if lawyer.isBlocked ==1:
                return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')


            clients = db.query(Clients, User).join(
                User, Clients.userId == User.id
            ).filter(
                Clients.lawyerId == lawyer.id,
                Clients.isDeleted == 0,
                Clients.isBlocked==0
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
                Staff.isBlocked == 0,
                Clients.isDeleted == 0,
                Clients.isBlocked ==0
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

        if user is None:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        if user.role not in ['lawyer','staff']:
            return APIHelper.send_forbidden_error(errorMessageKey='translations.FORBIDDEN')

        client = db.query(Clients).filter(Clients.id == client_id).first()
        if client is None:
                return APIHelper.send_not_found_error(errorMessageKey='translations.CLIENT_NOT_FOUND')
        if client.isDeleted==1 or client.isBlocked==1:
                return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED_OR_DELETED')

        #  LAWYER
        if user.role == 'lawyer':
            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
            if lawyer is None:
                return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')
            if lawyer.isBlocked == 1:
                return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')
            if client.lawyerId != lawyer.id:
                return APIHelper.send_forbidden_error(errorMessageKey='translations.NOT_ALLOWDED_TO_ACCESS_THIS_CLIENT')

        #  STAFF
        else:
            staff = db.query(Staff).filter(
                Staff.user_id == user.id,
                Staff.lawyerId == client.lawyerId,
                Staff.isBlocked == 0,
            ).first()
            if staff is None:
                return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED_OR_NOT_ASSIGNED_TO_LAWYER')
                
            if client.isBlocked == 1:
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

        client = db.query(Clients).filter(
            Clients.id == client_id,
            Clients.isDeleted == 0
        ).first()

        if client is None:
            return APIHelper.send_not_found_error(
                errorMessageKey='translations.CLIENT_NOT_FOUND'
            )

        if client.lawyerId != lawyer.id:
            return APIHelper.send_forbidden_error(
                errorMessageKey='translations.NOT_ALLOWED'
            )

        try:
            # 1. Soft delete client
            client.isDeleted = 1

            # 2. Get all cases of this client
            cases = db.query(Cases).filter(
                Cases.clientId == client_id,
                Cases.isDeleted == 0
            ).all()

            case_ids = [case.id for case in cases]

            # 3. Soft delete cases
            db.query(Cases).filter(
                Cases.id.in_(case_ids)
            ).update({"isDeleted": 1}, synchronize_session=False)

            # 4. Soft delete related tables
            db.query(Documents).filter(
                Documents.caseId.in_(case_ids)
            ).update({"isDeleted": 1}, synchronize_session=False)

            db.query(Tasks).filter(
                Tasks.caseId.in_(case_ids)
            ).update({"isDeleted": 1}, synchronize_session=False)

            db.query(CaseStatusHistories).filter(
                CaseStatusHistories.caseId.in_(case_ids)
            ).update({"isDeleted": 1}, synchronize_session=False)

            db.query(CourtSessions).filter(
                CourtSessions.caseId.in_(case_ids)
            ).update({"isDeleted": 1}, synchronize_session=False)

            db.query(Invoices).filter(
                Invoices.caseId.in_(case_ids)
            ).update({"isDeleted": 1}, synchronize_session=False)

            db.commit()

            return {"message": "Client and all related data soft deleted successfully"}

        except Exception as e:
            db.rollback()
            return APIHelper.send_bad_request_error(
                errorMessageKey='translations.DB_ERROR'
            )
    #  BLOCK CLIENT
    def block_client(client_id: int, user: UserModel, db: Session):

        if user is None:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        if user.role!='lawyer':
            return APIHelper.send_forbidden_error(errorMessageKey='translations.FORBIDDEN')

        lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()
        if lawyer is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')
        if lawyer.isBlocked == 1:
             return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')

        client = db.query(Clients).filter(Clients.id == client_id).first()
        if client is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.CLIENT_NOT_FOUND')
        if client.lawyerId != lawyer.id:
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        client.isBlocked = 1
        db.commit()
        return {"message": "Client blocked successfully"}
