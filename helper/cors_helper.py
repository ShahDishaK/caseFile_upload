from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware


class CORSHelper:

    def setup_cors(app: FastAPI):

        if os.getenv("ENV") == "development":
            origins =["*"]
        else:
            cors_domains = os.getenv("CORS_DOMAIN")
            origins = cors_domains.split(",") if cors_domains else []

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )