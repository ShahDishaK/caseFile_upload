# Loading the .env file
from dotenv import load_dotenv
from os.path import join, dirname
# from helper.api_helper import APIHelper
# from helper.cors_helper import CORSHelper
# from helper.logger_helper import setup_logger

# Setting up dotenv
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Importing libraries
from fastapi import FastAPI, Request
from controllers.user_controller import router
from controllers.case_controller import case
from fastapi import APIRouter
from controllers.auth_controller import auth
# from fastapi.exceptions import RequestValidationError
# import i18n

# #Setup Logger
# setup_logger()

# #Setup i18n
# i18n.load_path.append('language/')
# i18n.set("filename_format", "{namespace}.{locale}.{format}")
# i18n.set("file_format", "json")

# # Initializing app
from config.db_config import engine
from models.users_table import Base
app = FastAPI()
Base.metadata.create_all(bind=engine)

# #Setup CORS
# CORSHelper.setup_cors(app)

# # Request validation error
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     if exc.errors()[0]['type'] == 'value_error':
#         return APIHelper.send_error_response(
#             errorMessageKey =f"{exc.errors()[0]['msg']}"
#         )
#     else:
#         return APIHelper.send_error_response(
#             errorMessageKey =f"{exc.errors()[0]['loc'][1]} {exc.errors()[0]['msg']}")

# Including the routes
app.include_router(router)
app.include_router(auth)
app.include_router(case)



