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
from controllers.admin_controller import AdminController

admin=APIRouter(
    prefix='/admins',
    tags=['admins']
)

@admin.get("/dashboard/case-counts")
def case_counts(user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    return AdminController.get_case_counts(user,db)

@admin.get("/dashboard/status-counts")
def get_case_status_count(user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    return AdminController.get_case_status_count(user,db)

@admin.get("/dashboard/task-counts")
def task_count(user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    return AdminController.task_count(user,db)
