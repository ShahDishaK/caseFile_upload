# Importing libraries
from dtos.auth_models import UserModel
from helper.api_helper import APIHelper
from models.staff_table import Staff
from models.lawyers_table import Lawyers
from models.tasks_table import Tasks
from sqlalchemy.orm import Session
from dtos.task_models import TaskModel as CreateTaskRequest, UpdateTaskRequest

class TaskController:
    def create_task(create_task_request: CreateTaskRequest,user: UserModel,db: Session):
        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        create_document_model = Tasks(
            title=create_task_request.title,
            description=create_task_request.description,
            caseId=create_task_request.caseId,
            assignedTo=user.id,
            status=create_task_request.status,
            priority=create_task_request.priority
        )
        db.add(create_document_model)
        db.commit()
        return create_document_model

    def read_all(user: UserModel,db: Session ):
        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        if user.role=='lawyer':
            lawyer = db.query(Lawyers).filter(
                Lawyers.userId == user.id
            ).first()

            if not lawyer:
                return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')

            #  BLOCK
            if lawyer.isBlocked == b'\x01':
                return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')

            tasks= db.query(Tasks).filter(Tasks.assignedTo==user.id).all()
            return tasks
        
        elif user.role=='staff':
            staff = db.query(Staff).filter(
                Staff.user_id == user.id
            ).first()

            if not staff:
                return APIHelper.send_not_found_error(errorMessageKey='translations.STAFF_NOT_FOUND')

            #  BLOCK 
            if staff.isBlocked == b'\x01':
                return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')

            tasks= db.query(Tasks).filter(Tasks.assignedTo==user.id).all()
            return tasks



    def update_task(
        task_id: int,
        update_task_request: UpdateTaskRequest,
        user: UserModel ,
    db: Session
    ):
        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        task_model = db.query(Tasks).filter(Tasks.id == task_id).first()

        if task_model is None:
            return APIHelper.send_not_found_error(errorMessageKey='translations.TASK_NOT_FOUND')
        if task_model.assignedTo==user.id:
            update_data = update_task_request.dict(exclude_unset=True, exclude_none=True)

            for key, value in update_data.items():
                setattr(task_model, key, value)
            
            db.commit()
            db.refresh(task_model)

            return task_model
        return APIHelper.send_forbidden_error(errorMessageKey='translations.NOT_ASSIGNED_TO_THIS_TASK')


    # delete the document
    def delete_task(
        task_id: int,
        user: UserModel,
        db: Session
    ):
        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        task_model = db.query(Tasks).filter(Tasks.id == task_id).first()
        if not task_model:
            return APIHelper.send_not_found_error(errorMessageKey='translations.TASK_NOT_FOUND')
        if task_model.assignedTo==user.id:

            if task_model is None:
                return APIHelper.send_not_found_error(errorMessageKey='translations.TASK_NOT_FOUND')
            db.delete(task_model)
            db.commit()
            return {"message": "Document deleted successfully"}