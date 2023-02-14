# Importing libraries
from fastapi import APIRouter, Depends
from controllers.auth_controller import AuthController
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

# Declaring router
auth = APIRouter(tags=['Authentication'])

@auth.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends()):
    return AuthController.login(request)
