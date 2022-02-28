
from typing import List
from fastapi.exceptions import HTTPException
from fastapi import Depends

from fastapi_jwt_auth import AuthJWT


class ValidateUser:
    def __init__(self, allowed_roles: List[str] = None):
        self.allowed_roles:List[str] = allowed_roles
        self.current_user:str = ""
        self.user_roles:List[str]

    def __call__(self, authorize: AuthJWT = Depends()):
        authorize.jwt_required()
        self.user_roles = authorize.get_raw_jwt()['roles'].split(",")

        if(self.allowed_roles is not None) and not any(rol in self.allowed_roles for rol in self.user_roles):
            raise HTTPException(status_code=401, detail= "Usuario no autotizado")

        self.current_user = authorize.get_jwt_subject()
