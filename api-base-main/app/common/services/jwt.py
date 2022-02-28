from datetime import timedelta
from typing import Any, Dict

from fastapi_jwt_auth import AuthJWT
from pydantic import ValidationError
from common.config import SECRET_KEY
from fastapi import Depends

JWT_SUBJECT = "access"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=5)
REFRESH_TOKEN_EXPIRE_MINUTES = timedelta(minutes=30)


def create_access_token(subject:str, jwt_content: Dict[str, str], authorize: AuthJWT = AuthJWT()) -> str:
    return authorize.create_access_token(subject= subject, 
                                         expires_time=ACCESS_TOKEN_EXPIRE_MINUTES, 
                                         fresh=True,
                                         user_claims=jwt_content, 
                                         algorithm=ALGORITHM)

def create_refresh_token(subject:str, authorize: AuthJWT = AuthJWT()) -> str:
    return authorize.create_refresh_token(subject= subject, 
                                         expires_time=REFRESH_TOKEN_EXPIRE_MINUTES, 
                                         algorithm=ALGORITHM)

def decode_token(token:str, authorize: AuthJWT = AuthJWT()) -> Dict[str,str]:
    try:
        return authorize.get_raw_jwt(token)
    except ValidationError as validation_error:
        raise ValueError("malformed payload in token") from validation_error
