# Importing libraries
from typing import Optional
from dtos.auth_models import UserModel
from models.staff_table import Staff
from models.lawyers_table import Lawyers
from models.documents_table import Documents
from fastapi import APIRouter, Depends
from fastapi import Depends
from sqlalchemy.orm import Session
from config.db_config import dp_dependency, get_db
from typing_extensions import Annotated
from fastapi import APIRouter,Depends,HTTPException,Path
from starlette import status 
from helper.token_helper import TokenHelper
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from pydantic import BaseModel, Field
from dtos.document_models import DocumentModel as CreateDocumentRequest, UpdateDocumentRequest





class DocumentController:

    def create_document(create_document_request: CreateDocumentRequest,user: UserModel,db: Session):
        if user is None or user.role not in ['lawyer', 'staff']:
            raise HTTPException(status_code=401,detail='Authentication Failed')
        create_document_model = Documents(
            title=create_document_request.title,
            documentLink=create_document_request.documentLink,
            fileType=create_document_request.fileType,
            description=create_document_request.description,
            notes=create_document_request.notes,
            caseId=create_document_request.caseId,
            userId=user.id,
            clientId=create_document_request.clientId
        )
        db.add(create_document_model)
        db.commit()


    def read_all(user: UserModel,db: Session):
        if user is None or user.role not in ['lawyer', 'staff']:
            raise HTTPException(status_code=401,detail='Authentication Failed')
         # LAWYER
        if user.role == 'lawyer':

            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

            if lawyer is None:
                raise HTTPException(status_code=404, detail="Lawyer not found")

            documnets = db.query(Documents).filter(
                Documents.userId == lawyer.userId,
            ).all()

            return documnets

        # STAFF
        else:

            staff = db.query(Staff).filter(Staff.user_id == user.id).first()

            if staff is None:
                raise HTTPException(status_code=404, detail="Staff not found")

            documnets = db.query(Documents).filter(
                Documents.userId == staff.user_id,
            ).all()

            return documnets


    def update_document(
        document_id: int,
        update_document_request: UpdateDocumentRequest,
        user: UserModel ,
    db: Session 
    ):
        if user is None or user.role not in ['lawyer', 'staff']:
            raise HTTPException(status_code=401, detail='Authentication Failed')

        document_model = db.query(Documents).filter(Documents.id == document_id).first()

        if document_model is None:
            raise HTTPException(status_code=404, detail="Document not found")
        # LAWYER
        if user.role == 'lawyer':

            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

            if lawyer is None:
                raise HTTPException(status_code=404, detail="Lawyer not found")
            if Documents.userId==lawyer.userId:
                update_data = update_document_request.dict(exclude_unset=True, exclude_none=True)

                for key, value in update_data.items():
                    setattr(document_model, key, value)
                
                db.commit()
                db.refresh(document_model)

                return document_model
        else:
            staff = db.query(Staff).filter(Staff.user_id == user.id).first()

            if staff is None:
                raise HTTPException(status_code=404, detail="Staff not found")
            
            if Documents.userId==staff.user_id:
                update_data = update_document_request.dict(exclude_unset=True, exclude_none=True)

                for key, value in update_data.items():
                    setattr(document_model, key, value)
                
                db.commit()
                db.refresh(document_model)

                return document_model



# delete the document
    def delete_document(
        document_id: int,
        user: UserModel ,
        db: Session 
    ):
        if user is None or user.role not in ['lawyer', 'staff']:
            raise HTTPException(status_code=401, detail='Authentication Failed')
        
        document_model = db.query(Documents).filter(Documents.id == document_id).first()

        if document_model is None:
            raise HTTPException(status_code=404, detail="Document not found")
        # LAWYER
        if user.role == 'lawyer':

            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

            if lawyer is None:
                raise HTTPException(status_code=404, detail="Lawyer not found")
            if Documents.userId==lawyer.userId:
                Documents.delete(document_model)
                db.commit()
                return {"message": "Document deleted successfully"}
            
        else:
            staff = db.query(Staff).filter(Staff.user_id == user.id).first()

            if staff is None:
                raise HTTPException(status_code=404, detail="Staff not found")
            
            if Documents.userId==staff.user_id:
                Documents.delete(document_model)
                db.commit()
                return {"message": "Document deleted successfully"}
            