# Importing libraries
from dtos.auth_models import UserModel
from fastapi import APIRouter, Depends
from fastapi import Depends
from sqlalchemy.orm import Session
from config.db_config import get_db
from typing_extensions import Annotated
from fastapi import APIRouter,Depends
from starlette import status 
from helper.token_helper import TokenHelper
from dtos.document_models import DocumentModel as CreateDocumentRequest, UpdateDocumentRequest
from controllers.document_controller import DocumentController

document=APIRouter(
    prefix='/documents',
    tags=['document']
)



user_dependency=Annotated[dict,Depends(TokenHelper.get_current_user)]

@document.post("/document", status_code=status.HTTP_201_CREATED)
async def create_document(create_document_request: CreateDocumentRequest,user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    return DocumentController.create_document(create_document_request,user,db)

@document.get("/",status_code=status.HTTP_200_OK)
async def read_all(user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    return DocumentController.read_all(user,db)

@document.post("/document", status_code=status.HTTP_201_CREATED)
async def create_document(create_document_request: CreateDocumentRequest,user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    return DocumentController.create_document(create_document_request,user,db)

@document.patch("/document/{document_id}", status_code=status.HTTP_200_OK)
async def update_document(
    document_id: int,
    update_document_request: UpdateDocumentRequest,
    user: UserModel = Depends(TokenHelper.get_current_user),
   db: Session = Depends(get_db)
):
    return DocumentController.update_document(document_id,update_document_request,user,db)

@document.delete("/document/{document_id}", status_code=status.HTTP_200_OK)
async def delete_document(
    document_id: int,
    user: UserModel = Depends(TokenHelper.get_current_user),
    db: Session = Depends(get_db)
):
    return DocumentController.delete_document(document_id,user,db)