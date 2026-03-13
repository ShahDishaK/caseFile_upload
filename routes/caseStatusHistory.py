from typing import Optional
from dtos.auth_models import UserModel
from helper.api_helper import APIHelper
from models.cases_table import Cases
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
from dtos.case_models import CaseModel as CreateCaseRequest, UpdateCaseRequest
from controllers.caseStatusHistory_controller import CaseController

caseStatus=APIRouter(
    prefix='/caseStatus',
    tags=['caseStatus']
)

@caseStatus.post("/case", status_code=status.HTTP_201_CREATED)
async def create_case(create_case_request: CreateCaseRequest,user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    return CaseController.create_case(create_case_request,user,db)

@caseStatus.get("/",status_code=status.HTTP_200_OK)
async def read_all(user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    return CaseController.create_case(user,db)

@caseStatus.patch("/case/{case_id}", status_code=status.HTTP_200_OK)
async def update_case(case_id: int,update_case_request: UpdateCaseRequest,user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    return CaseController.create_case(case_id,update_case_request,user,db)

@caseStatus.delete("/case/{case_id}", status_code=status.HTTP_200_OK)
async def delete_case(case_id: int, user: UserModel = Depends(TokenHelper.get_current_user), db: Session = Depends(get_db)):
    return CaseController.create_case(case_id,user,db)
