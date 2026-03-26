from dtos.auth_models import UserModel
from fastapi import APIRouter, Depends
from fastapi import Depends
from sqlalchemy.orm import Session
from config.db_config import  get_db
from fastapi import APIRouter,Depends
from starlette import status 
from helper.token_helper import TokenHelper
from dtos.case_models import CaseModel as CreateCaseRequest, UpdateCaseRequest
from controllers.case_controller import CaseController

case=APIRouter(
    prefix='/cases',
    tags=['cases']
)

@case.post("/case", status_code=status.HTTP_201_CREATED)
async def create_case(create_case_request: CreateCaseRequest,user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    return CaseController.create_case(create_case_request,user,db)

@case.get("/",status_code=status.HTTP_200_OK)
async def read_all(user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    return CaseController.read_all(user,db)

@case.patch("/case/{case_id}", status_code=status.HTTP_200_OK)
async def update_case(case_id: int,update_case_request: UpdateCaseRequest,user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    return CaseController.update_case(case_id,update_case_request,user,db)

@case.delete("/{case_id}", status_code=status.HTTP_200_OK)
async def soft_delete_case(case_id: int, user: UserModel = Depends(TokenHelper.get_current_user), db: Session = Depends(get_db)):
    return CaseController.soft_delete_case(case_id,user,db)
