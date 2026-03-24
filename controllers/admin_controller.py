# Importing libraries
from dtos.auth_models import UserModel
from models.companies_table import Companies
from models.users_table import User, UserRole
from helper.api_helper import APIHelper
from models.cases_table import Cases
from models.caseStatusHistory_table import CaseStatusHistories
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models.cases_table import Cases, CaseStatus
from sqlalchemy import  func
from models.tasks_table import Tasks, TaskStatus
import os
import i18n

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
i18n.load_path.append(os.path.join(BASE_DIR, 'language'))
i18n.set('filename_format', '{namespace}.{locale}.{format}')
i18n.set('fallback', 'en')
i18n.set('locale', 'en')

class AdminController:
    # open cases, closed cases, and new cases in the last 30 days counts
    def get_case_counts(user: UserModel,db: Session):
        if user is None or user.role != "admin":
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        open_cases = db.query(func.count(Cases.id)).filter(
            Cases.status == CaseStatus.open,
            Cases.isDeleted == b'\x00'
        ).scalar()
        
        closed_cases = db.query(func.count(Cases.id)).filter(
            Cases.status == CaseStatus.closed,
            Cases.isDeleted == b'\x00'
        ).scalar()
        
        new_cases = db.query(func.count(Cases.id)).filter(
            Cases.createdAt >= thirty_days_ago,
            Cases.isDeleted ==b'\x00'
        ).scalar()

        return {
            "openCases": open_cases,
            "closedCases": closed_cases,
            "newCasesLast30Days": new_cases
        }
    
    # case status count
    def get_case_status_count(user:UserModel,db:Session):
        if user is None or user.role!='admin':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        
        last_thirty_days=datetime.utcnow()-timedelta(days=30)
        
        closed_last_30_days=db.query(func.count(CaseStatusHistories.id)).filter(
            CaseStatusHistories.updatedAt>=last_thirty_days,
        ).scalar()

        return {
        "casesStatusChangeInLast30Days": closed_last_30_days
        }
    
    # task count based on due
    def task_counts(user:UserModel,db: Session):
        if user is None or user.role!='admin':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        today_tasks = db.query(func.count(Tasks.id)).filter(
            Tasks.status == TaskStatus.TODAY
        ).scalar()

        overdue_tasks = db.query(func.count(Tasks.id)).filter(
            Tasks.status == TaskStatus.OVERDUE
        ).scalar()

        completed_tasks = db.query(func.count(Tasks.id)).filter(
            Tasks.status == TaskStatus.COMPLETED
        ).scalar()

        return {
            "dueToday": today_tasks,
            "overdue": overdue_tasks,
            "completed": completed_tasks
        }
    
    def company_users(company_id: int, user: UserModel, db: Session):

        if user is None or user.role != 'admin':
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        company = db.query(Companies).filter(Companies.id == company_id).first()

        if company is None:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        lawyers = db.query(User).filter(
            User.companyId == company_id,
            User.role == UserRole.LAWYER,
            User.isDeleted.is_(False)
        ).all()

        staff = db.query(User).filter(
            User.companyId == company_id,
            User.role == UserRole.STAFF,
            User.isDeleted.is_(False)
        ).all()

        return {
            "companyId": company.id,
            "companyName": company.name,
            "lawyers": lawyers,
            "staff": staff
        }