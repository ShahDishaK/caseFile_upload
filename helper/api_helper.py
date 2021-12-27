# Importing libraries
from typing import Any, Optional
from fastapi.responses import JSONResponse
from schemas.base_response_model import BaseResponseModel
import i18n

class APIHelper:
    # Send success response with custom message
    def send_error_response(errorMessageKey: Optional[str] = None, locale: Optional[str] = "en"):
        return JSONResponse(
            status_code=400, content=(BaseResponseModel(error=i18n.t(key= errorMessageKey or 'translations.FAILURE',locale=locale)).__dict__),
        )

    # Send unauthorized response with custom message
    def send_unauthorized_error(locale: Optional[str] = "en"):
        return JSONResponse(
            status_code=401,
            content=(BaseResponseModel(error=i18n.t('translations.UNAUTHORIZED',locale=locale))),
        )

    # Send error response with custom message
    def send_success_response(
        data: Optional[Any] = None, successMessageKey: Optional[str] = None, locale: Optional[str] = "en"
    ):
        return BaseResponseModel(data=data, message= i18n.t(key= successMessageKey or  'translations.SUCCESS',locale=locale))
