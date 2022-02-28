from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi_jwt_auth.auth_jwt import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from common.api.errors.http_error import http_error_handler
from common.api.errors.jwt_errors import authjwt_exception_handler
from common.api.errors.validation_error import http422_error_handler
from model.errors import EntityNotFoundException, http420_error_handler
from routes.api import api_router
from common.config import ALLOWED_HOSTS, API_PREFIX, DEBUG, JWTSettings
from db import orm

def get_application() -> FastAPI:
    application = FastAPI(title="Proyecto Microservicios", debug=DEBUG, version="1.0")

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.add_exception_handler(AuthJWTException, authjwt_exception_handler)
    application.add_exception_handler(EntityNotFoundException, http420_error_handler)

    application.include_router(api_router, prefix=API_PREFIX)

    return application

app = get_application()
@AuthJWT.load_config
def get_config():
    return JWTSettings()
orm.start_mappers()