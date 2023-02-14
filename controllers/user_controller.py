# Importing libraries
from dtos.auth_models import UserModel
from dtos.base_response_model import BaseResponseModel
from dtos.user_models import CreateUserModel
from helper.api_helper import APIHelper
from config.db_config import engine
from helper.hashing import Hash
from models.users_table import users_table


class UserController:
    def create_user(request: CreateUserModel) -> BaseResponseModel:
        with engine.connect() as db:
            password = Hash.get_hash(request.password)
            new_user = db.execute(users_table.insert().values(
                email=request.email, password=password, is_admin=request.is_admin).returning()).fetchone()
        return APIHelper.send_success_response(data=UserModel(**new_user), successMessageKey='translations.USER_CREATED')

    def delete_user(user_id: int) -> BaseResponseModel:
        with engine.connect() as db:
            db.execute(users_table.delete().where(users_table.c.id == id))
        return APIHelper.send_success_response(successMessageKey='translations.USER_DELETED')

    def get_users(page: int, size: int) -> BaseResponseModel:
        with engine.connect() as db:
            users = db.execute(users_table.select().offset(
                (page - 1) * size).limit(size)).fetchall()
        return APIHelper.send_success_response(data=users, successMessageKey='translations.SUCCESS')
