from sqlalchemy.orm import Session
from helper.api_helper import APIHelper
from models.companies_table import Companies
from dtos.company_models import CompanyModel, UpdateCompanyRequest
from dtos.auth_models import UserModel

class CompanyController:

   
    def create_company(create_company_request: CompanyModel, user: UserModel, db: Session):
        if user is None:
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        if user.role!='admin':
            return APIHelper.send_forbidden_error(errorMessageKey='translations.FORBIDDEN')

        company = Companies(
            name=create_company_request.name,
            Address=create_company_request.Address,
            phoneNumber=create_company_request.phoneNumber,
            email=create_company_request.email
        )

        db.add(company)
        db.commit()
        db.refresh(company)

        response_data={"company":company}
        return APIHelper.send_success_response(
                    data=response_data,
                    successMessageKey='translations.SUCCESS'
                )


   
    def read_all(user: UserModel, db: Session):
        if user is None:
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        if user.role!='admin':
            return APIHelper.send_forbidden_error(errorMessageKey='translations.FORBIDDEN')

        company= db.query(Companies).all()
        response_data={"company":company}
        return APIHelper.send_success_response(
                    data=response_data,
                    successMessageKey='translations.SUCCESS'
                )



   
    def update_company(company_id: int, update_company_request: UpdateCompanyRequest, user: UserModel, db: Session):

        if user is None:
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        if user.role!='admin':
            return APIHelper.send_forbidden_error(errorMessageKey='translations.FORBIDDEN')

        company = db.query(Companies).filter(Companies.id == company_id).first()

        if company is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.COMPANY_NOT_FOUND')

        update_data = update_company_request.dict(exclude_unset=True, exclude_none=True)

        for key, value in update_data.items():
            setattr(company, key, value)

        db.commit()
        db.refresh(company)

        response_data={"company":company}
        return APIHelper.send_success_response(
                    data=response_data,
                    successMessageKey='translations.SUCCESS'
                )
    
    def delete_company(company_id: int, user: UserModel, db: Session):

        if user is None:
            APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        if user.role!='admin':
            return APIHelper.send_forbidden_error(errorMessageKey='translations.FORBIDDEN')

        company = db.query(Companies).filter(Companies.id == company_id).first()

        if company is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.COMAPNY_NOT_FOUND')

        db.delete(company)
        db.commit()

        response_data= {"message": "Company deleted successfully"}
        return APIHelper.send_success_response(
                    data=response_data,
                    successMessageKey='translations.SUCCESS'
                )