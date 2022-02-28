from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth.exceptions import AccessTokenRequired, AuthJWTException, CSRFError, FreshTokenRequired, InvalidHeaderError, JWTDecodeError, MissingTokenError, RefreshTokenRequired, RevokedTokenError
from starlette.responses import JSONResponse


def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    status_code = exc.status_code
    if isinstance(exc, InvalidHeaderError):
        status_code = 411
    if isinstance(exc, JWTDecodeError):
        status_code = 412
    if isinstance(exc, CSRFError):
        status_code = 413
    if isinstance(exc, MissingTokenError):
        status_code = 414
    if isinstance(exc, RevokedTokenError):
        status_code = 415
    if isinstance(exc, AccessTokenRequired):
        status_code = 416
    if isinstance(exc, RefreshTokenRequired):
        status_code = 417
    if isinstance(exc, FreshTokenRequired):
        status_code = 418
    
    return JSONResponse(
        status_code = status_code,
        content={"message":exc.message, "status":status_code, "details": str(jsonable_encoder(exc))}
    )
