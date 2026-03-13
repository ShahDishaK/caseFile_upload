from fastapi import HTTPException
from starlette import status
from sqlalchemy.orm import Session
from models.companies_table import Companies
from dtos.company_models import CompanyModel, UpdateCompanyRequest
from dtos.auth_models import UserModel


class CompanyController:

   
    def create_company(create_company_request: CompanyModel, user: UserModel, db: Session):
        if user is None or user.role != 'admin':
            raise HTTPException(status_code=401, detail="Authentication Failed")

        company = Companies(
            name=create_company_request.name,
            Address=create_company_request.Address,
            phoneNumber=create_company_request.phoneNumber,
            email=create_company_request.email
        )

        db.add(company)
        db.commit()
        db.refresh(company)

        return company


   
    def read_all(user: UserModel, db: Session):
        if user is None or user.role != 'admin':
            raise HTTPException(status_code=401, detail="Authentication Failed")

        return db.query(Companies).all()


   
    def update_company(company_id: int, update_company_request: UpdateCompanyRequest, user: UserModel, db: Session):

        if user is None or user.role != 'admin':
            raise HTTPException(status_code=401, detail="Authentication Failed")

        company = db.query(Companies).filter(Companies.id == company_id).first()

        if company is None:
            raise HTTPException(status_code=404, detail="Company not found")

        update_data = update_company_request.dict(exclude_unset=True, exclude_none=True)

        for key, value in update_data.items():
            setattr(company, key, value)

        db.commit()
        db.refresh(company)

        return company