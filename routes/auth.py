#Importing libraries
from fastapi import APIRouter, Request
from controllers.auth_controller import AuthController
from schemas.auth_models import LoginRequest

# Declaring router
auth = APIRouter(tags=['Authentication'])

# Login API
@auth.post('/login')
def login(user: LoginRequest, request: Request):
    return AuthController.login(request=user, locale= request.headers['accept-language'])
