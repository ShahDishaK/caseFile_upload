# Importing libraries
from typing import Optional
from dtos.auth_models import UserModel
from helper.api_helper import APIHelper
from models.staff_table import Staff
from fastapi import APIRouter, Depends
from fastapi import Depends
from sqlalchemy.orm import Session
from config.db_config import get_db
from typing_extensions import Annotated
from fastapi import APIRouter,Depends,HTTPException,Path
from starlette import status 
from helper.token_helper import TokenHelper
from pydantic import Field
from dtos.staff_models import StaffModel as CreateStaffRequest, UpdateStaffRequest

staff=APIRouter(
    prefix='/staff',
    tags=['staff']
)


user_dependency=Annotated[dict,Depends(TokenHelper.get_current_user)]

@staff.post("/staff", status_code=status.HTTP_201_CREATED)
async def create_task(create_staff_request: CreateStaffRequest,user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    if user is None or user.role !='lawyer':
        raise HTTPException(status_code=401,detail='Authentication Failed')
    create_staff_model = Staff(
        user_id=create_staff_request.user_id,
        caseId=create_staff_request.caseId,
        lawyerId=create_staff_request.lawyerId,
        taskId=create_staff_request.taskId,
        isBlocked=create_staff_request.isBlocked
    )
    db.add(create_staff_model)
    db.commit()
    db.add(create_staff_model)
    db.commit()

def active_staff(db):
    return db.query(Staff).filter(Staff.isBlocked.is_(False))


@staff.get("/",status_code=status.HTTP_200_OK)
async def read_all(user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    if user is None or user.role !='lawyer':
        raise HTTPException(status_code=401,detail='Authentication Failed')
    staff = active_staff(Staff).all()
    return staff

@staff.patch("/staff/{staff_id}", status_code=status.HTTP_200_OK)
async def update_staff(
    staff_id: int,
    update_staff_request: UpdateStaffRequest,
    user: UserModel = Depends(TokenHelper.get_current_user),
   db: Session = Depends(get_db)
):
    if user is None or user.role !='lawyer':
        raise HTTPException(status_code=401, detail='Authentication Failed')

    staff_model = db.query(Staff).filter(Staff.id == staff_id).first()

    if staff_model is None:
        raise HTTPException(status_code=404, detail="Document not found")

    update_data = update_staff_request.dict(exclude_unset=True, exclude_none=True)

    for key, value in update_data.items():
        setattr(staff_model, key, value)
    
    db.commit()
    db.refresh(staff_model)

    return staff_model

# delete the document
@staff.delete("/staff/{staff_id}", status_code=status.HTTP_200_OK)
async def delete_staff(
    staff_id: int,
    user: UserModel = Depends(TokenHelper.get_current_user),
    db: Session = Depends(get_db)
):
    if user is None or user.role !='lawyer':
        raise HTTPException(status_code=401, detail='Authentication Failed')

    staff_model = db.query(Staff).filter(Staff.id == staff_id).first()
    if staff_model is None:
        raise HTTPException(status_code=404, detail="Document not found")
    Staff.delete(staff_model)
    db.commit()
    return {"message": "Document deleted successfully"}

# Block staff
@staff.put("/staff/{client_id}/block", status_code=status.HTTP_200_OK)
async def block_staff(client_id: int, user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):

    if user is None or user.role != "lawyer":
        return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

    db.query(Staff).filter(Staff.id == client_id).update(
        {"isBlocked": True}
    )

    db.commit()

    return {"message": "Client blocked successfully"}