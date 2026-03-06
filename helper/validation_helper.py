# import i18n
# import re
# from config.constants import Constants
# from helper.api_helper import APIHelper
# from utils.db_helper import DBHelper
from config.db_config import dp_dependency
from models.users_table import User
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ValidationHelper:
    def authenticate_user(username: str, password: str, db):
        user = db.query(User).filter(User.name == username).first()
        print(user)
        if user is None:
            return False
        print(bcrypt_context.verify(password, user.password))
        if not bcrypt_context.verify(password, user.password):
            return False
        return user

#     def is_valid_email(cls, v):
#         if not re.fullmatch(Constants.EMAIL_REGEX, v):
#             raise ValueError(i18n.t(key='translations.INVALID_EMAIL'))
#         user = DBHelper.get_user_by_email(v)
#         if user:
#             raise APIHelper.send_error_response(errorMessageKey='translations.USER_EXISTS')
#         return v

#     def is_mobile(cls, v):
#         if not re.fullmatch(Constants.MOBILE_NUMBER_REGEX, v):
#             raise ValueError(i18n.t(key='translations.INVALID_MOBILE'))
#         return v

#     def is_valid_password(cls, v):
#         if not re.fullmatch(Constants.PASSWORD_REGEX, v):
#             raise ValueError(i18n.t(key='translations.INVALID_PASSWORD'))
#         return v
