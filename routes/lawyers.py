from controllers.lawyer_controller import LawyerController
from dtos.lawyer_models import LawyerModel as CreateLawyerRequest, UpdateLawyerRequest
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from config.db_config import get_db
from helper.token_helper import TokenHelper
from dtos.auth_models import UserModel

lawyer=APIRouter(
    prefix='/lawyers',
    tags=['lawyers']
)

@lawyer.post("/lawyer", status_code=status.HTTP_201_CREATED)
async def create_lawyer(create_lawyer_request: CreateLawyerRequest,user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    return LawyerController.create_lawyer(create_lawyer_request,user,db)

@lawyer.get("/",status_code=status.HTTP_200_OK)
async def read_all(user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
    return LawyerController.read_all(user,db)

@lawyer.patch("/lawyer/{client_id}", status_code=status.HTTP_200_OK)
async def update_lawyer(client_id: int,update_client_request: UpdateLawyerRequest,user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
        return LawyerController.update_lawyer(client_id,update_client_request,user,db)
    
@lawyer.delete("/lawyer/{client_id}", status_code=status.HTTP_200_OK)
async def delete_lawyer(client_id: int, user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
        return LawyerController.delete_lawyer(client_id,user,db)

@lawyer.put("/lawyer/{client_id}/block", status_code=status.HTTP_200_OK)
async def block_lawyer(client_id: int, user: UserModel = Depends(TokenHelper.get_current_user),db: Session = Depends(get_db)):
        return LawyerController.block_lawyer(client_id,user,db)
