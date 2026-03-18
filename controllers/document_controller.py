# Importing libraries
from dtos.auth_models import UserModel
from helper.api_helper import APIHelper
from models.staff_table import Staff
from models.lawyers_table import Lawyers
from models.documents_table import Documents
from models.cases_table import Cases
from sqlalchemy.orm import Session
from fastapi import HTTPException
from dtos.document_models import DocumentModel as CreateDocumentRequest, UpdateDocumentRequest
import base64
import requests
import os

class DocumentController:

    #  CREATE DOCUMENT
    def create_document(create_document_request: CreateDocumentRequest, user: UserModel, db: Session):

        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        #  LAWYER CHECK
        if user.role == 'lawyer':
            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

            if lawyer is None:
                raise HTTPException(status_code=404, detail="Lawyer not found")

            if lawyer.isBlocked == b'\x01':
                raise HTTPException(status_code=403, detail="You are blocked")

        #  STAFF CHECK
        else:
            staff = db.query(Staff).filter(
                Staff.user_id == user.id,
                Staff.caseId == create_document_request.caseId,
                Staff.isBlocked ==b'\x00'
            ).first()

            if staff is None:
                raise HTTPException(
                    status_code=403,
                    detail="You are blocked or not assigned to this case"
                )


        base64_content = None
        doc_link = create_document_request.documentLink

        try:
            if doc_link.startswith("http://") or doc_link.startswith("https://"):
                # Fetch file from URL
                response = requests.get(doc_link)
                if response.status_code == 200:
                    base64_content = base64.b64encode(response.content).decode('utf-8')
                else:
                    raise HTTPException(status_code=400, detail="Cannot fetch document from the link")
            else:
                # Local file path
                if not os.path.isfile(doc_link):
                    raise HTTPException(status_code=400, detail="Local file not found")
                
                with open(doc_link, "rb") as f:
                    base64_content = base64.b64encode(f.read()).decode('utf-8')
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error converting document to Base64: {str(e)}")

        # 🔹 Save document in DB
        document = Documents(
            title=create_document_request.title,
            documentLink=base64_content,  # store Base64
            fileType=create_document_request.fileType,
            description=create_document_request.description,
            notes=create_document_request.notes,
            caseId=create_document_request.caseId,
            userId=user.id,
            clientId=create_document_request.clientId
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document


    #  READ ALL DOCUMENTS
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

            documents = db.query(Documents).join(
                Cases, Documents.caseId == Cases.id
            ).filter(
                Cases.lawyerId == lawyer.id
            ).all()

            return documents

        #  STAFF
        else:
            documents = db.query(Documents).join(
                Cases, Documents.caseId == Cases.id
            ).join(
                Staff, Staff.caseId == Cases.id
            ).filter(
                Staff.user_id == user.id,
                Staff.isBlocked == b'\x00'
            ).all()

            if not documents:
                raise HTTPException(
                    status_code=403,
                    detail="You are blocked or no documents available"
                )

            return documents


    #  UPDATE DOCUMENT
    def update_document(document_id: int, update_document_request: UpdateDocumentRequest, user: UserModel, db: Session):

        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        document = db.query(Documents).filter(Documents.id == document_id).first()

        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")

        #  LAWYER
        if user.role == 'lawyer':
            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

            if lawyer is None:
                raise HTTPException(status_code=404, detail="Lawyer not found")

            if lawyer.isBlocked == b'\x01':
                raise HTTPException(status_code=403, detail="You are blocked")

            case = db.query(Cases).filter(Cases.id == document.caseId).first()

            if case.lawyerId != lawyer.id:
                return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        #  STAFF
        else:
            staff = db.query(Staff).filter(
                Staff.user_id == user.id,
                Staff.caseId == document.caseId,
                Staff.isBlocked == b'\x00'
            ).first()

            if staff is None:
                raise HTTPException(
                    status_code=403,
                    detail="You are blocked or not assigned to this case"
                )

        #  UPDATE
        update_data = update_document_request.dict(exclude_unset=True, exclude_none=True)

        for key, value in update_data.items():
            setattr(document, key, value)

        db.commit()
        db.refresh(document)

        return document


    #  DELETE DOCUMENT
    def delete_document(document_id: int, user: UserModel, db: Session):

        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        document = db.query(Documents).filter(Documents.id == document_id).first()

        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")

        #  LAWYER
        if user.role == 'lawyer':
            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

            if lawyer is None:
                raise HTTPException(status_code=404, detail="Lawyer not found")

            if lawyer.isBlocked == b'\x01':
                raise HTTPException(status_code=403, detail="You are blocked")

            case = db.query(Cases).filter(Cases.id == document.caseId).first()

            if case.lawyerId != lawyer.id:
                raise HTTPException(status_code=403, detail="Not authorized")

        #  STAFF
        else:
            staff = db.query(Staff).filter(
                Staff.user_id == user.id,
                Staff.caseId == document.caseId,
                Staff.isBlocked == b'\x00'
            ).first()

            if staff is None:
                raise HTTPException(
                    status_code=403,
                    detail="You are blocked or not assigned to this case"
                )

        db.delete(document)
        db.commit()

        return {"message": "Document deleted successfully"}