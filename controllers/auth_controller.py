# Importing libraries
from helper.api_helper import APIHelper
from schemas.auth_models import LoginRequest

class AuthController:
    
    """This is a example of a login method"""
    """Please update or add methods according to you need"""

    # Login api implementation
    def login(request: LoginRequest, locale: str = "en"):
        return APIHelper.send_success_response(locale=locale)