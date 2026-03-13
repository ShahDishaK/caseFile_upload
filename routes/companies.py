from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from config.db_config import get_db
from helper.token_helper import TokenHelper
from dtos.auth_models import UserModel
from dtos.company_models import CompanyModel, UpdateCompanyRequest
from controllers.company_controller import CompanyController

company = APIRouter(
    prefix="/company",
    tags=["Company"]
)


@company.post("/", status_code=status.HTTP_201_CREATED)
async def create_company(
    request: CompanyModel,
    user: UserModel = Depends(TokenHelper.get_current_user),
    db: Session = Depends(get_db)
):
    return CompanyController.create_company(request, user, db)


@company.get("/", status_code=status.HTTP_200_OK)
async def read_all(
    user: UserModel = Depends(TokenHelper.get_current_user),
    db: Session = Depends(get_db)
):
    return CompanyController.read_all(user, db)


@company.patch("/{company_id}", status_code=status.HTTP_200_OK)
async def update_company(
    company_id: int,
    request: UpdateCompanyRequest,
    user: UserModel = Depends(TokenHelper.get_current_user),
    db: Session = Depends(get_db)
):
    return CompanyController.update_company(company_id, request, user, db)