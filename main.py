# Loading the .env file
from dotenv import load_dotenv
from os.path import join, dirname
from helper.cors_helper import CORSHelper
from fastapi import FastAPI, Request
from controllers.user_controller import router
from controllers.case_controller import case
from controllers.document_controller import document
from fastapi import APIRouter
from controllers.auth_controller import auth
from config.db_config import engine
from models.users_table import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
CORSHelper.setup_cors(app)

app.include_router(router)
app.include_router(auth)
app.include_router(case)
app.include_router(document)




