# Importing libraries
from typing import Optional
from dtos.auth_models import UserModel
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
            raise HTTPException(status_code=401,detail='Authentication Failed')
        create_document_model = Tasks(
            title=create_task_request.title,
            description=create_task_request.description,
            caseId=create_task_request.caseId,
            assignedTo=create_task_request.assignedTo,
            status=create_task_request.status,
        )
        db.add(create_document_model)
        db.commit()

    def read_all(user: UserModel,db: Session ):
        if user is None or user.role not in ['lawyer', 'staff']:
            raise HTTPException(status_code=401,detail='Authentication Failed')
        documents = db.query(Tasks).all()
        return documents



    def update_task(
        task_id: int,
        update_task_request: UpdateTaskRequest,
        user: UserModel ,
    db: Session
    ):
        if user is None or user.role not in ['lawyer', 'staff']:
            raise HTTPException(status_code=401, detail='Authentication Failed')

        task_model = db.query(Tasks).filter(Tasks.id == task_id).first()

        if task_model is None:
            raise HTTPException(status_code=404, detail="Document not found")

        update_data = update_task_request.dict(exclude_unset=True, exclude_none=True)

        for key, value in update_data.items():
            setattr(task_model, key, value)
        
        db.commit()
        db.refresh(task_model)

        return task_model


    # delete the document
    def delete_task(
        task_id: int,
        user: UserModel,
        db: Session
    ):
        if user is None or user.role not in ['lawyer', 'staff']:
            raise HTTPException(status_code=401, detail='Authentication Failed')

        task_model = db.query(Tasks).filter(Tasks.id == task_id).first()

        if task_model is None:
            raise HTTPException(status_code=404, detail="Document not found")
        Tasks.delete(task_model)
        db.commit()
        return {"message": "Document deleted successfully"}