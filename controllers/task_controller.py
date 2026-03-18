# Importing libraries
from typing import Optional
from dtos.auth_models import UserModel
from helper.api_helper import APIHelper
from models.staff_table import Staff
from models.lawyers_table import Lawyers
from models.tasks_table import Tasks
from fastapi import APIRouter, Depends
from fastapi import Depends
from sqlalchemy.orm import Session
from config.db_config import get_db
from typing_extensions import Annotated
from fastapi import APIRouter,Depends,HTTPException,Path
from starlette import status 
from helper.token_helper import TokenHelper
from pydantic import Field
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
        )
        db.add(create_document_model)
        db.commit()

    def read_all(user: UserModel,db: Session ):
        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')
        if user.role=='lawyer':
            lawyer = db.query(Lawyers).filter(
                Lawyers.userId == user.id
            ).first()

            if not lawyer:
                raise HTTPException(status_code=404, detail="Lawyer not found")

            # ✅ BLOCK CHECK FIXED
            if lawyer.isBlocked == b'\x01':
                raise HTTPException(status_code=403, detail="You are blocked")

            tasks= db.query(Tasks).filter(Tasks.assignedTo==user.id).all()
            return tasks
        
        elif user.role=='staff':
            staff = db.query(Staff).filter(
                staff.userId == user.id
            ).first()

            if not staff:
                raise HTTPException(status_code=404, detail="Lawyer not found")

            # ✅ BLOCK CHECK FIXED
            if staff.isBlocked == b'\x01':
                raise HTTPException(status_code=403, detail="You are blocked")

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
            raise HTTPException(status_code=404, detail="Document not found")
        if task_model.assignedTo==user.id:
            update_data = update_task_request.dict(exclude_unset=True, exclude_none=True)

            for key, value in update_data.items():
                setattr(task_model, key, value)
            
            db.commit()
            db.refresh(task_model)

            return task_model
        raise HTTPException(status_code=403, detail="Forbidden: You are not assigned to this task")


    # delete the document
    def delete_task(
        task_id: int,
        user: UserModel,
        db: Session
    ):
        if user is None or user.role not in ['lawyer', 'staff']:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        task_model = db.query(Tasks).filter(Tasks.id == task_id).first()
        if task_model.assignedTo==user.id:

            if task_model is None:
                raise HTTPException(status_code=404, detail="Document not found")
            db.delete(task_model)
            db.commit()
            return {"message": "Document deleted successfully"}