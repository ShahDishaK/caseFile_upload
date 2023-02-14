# Importing libraries
from typing import Optional
from fastapi import APIRouter, Depends
from config.constants import Constants
from controllers.user_controller import UserController
from dtos.user_models import CreateUserModel
from helper.api_helper import APIHelper
from helper.token_helper import TokenHelper

# Declaring router
user = APIRouter(tags=['User'])

# Login API


@user.post('/user')
async def create_user(request: CreateUserModel = Depends(TokenHelper.get_current_user)):
    return UserController.create_user(request)


@user.get('/user')
async def get_user(user: str = Depends(TokenHelper.get_current_user)):
    return APIHelper.send_success_response(data=user, successMessageKey='translations.SUCCESS')


@user.delete('/user/{user_id}')
async def delete_user(user_id: int, _: str = Depends(TokenHelper.get_current_user)):
    return UserController.delete_user(user_id)


@user.get('/users')
async def get_users(page: int, size: Optional[int] = Constants.PAGE_SIZE, _: str = Depends(TokenHelper.get_current_user)):
    return UserController.get_users(page, size)
