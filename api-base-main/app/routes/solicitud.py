from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import errors
from pydantic.error_wrappers import ValidationError
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from model.domain.celular_prospecto_model import CelularProspectoModel
from model.errors import EntityNotFoundException
from model.errors import NotFoundMessage
from services import solicitud_handler as handler
from fastapi import Request
from fastapi_jwt_auth import AuthJWT
from common.api.responses import responses as HTTP_RESPONSES
import time
from loguru import logger


################################################################################
### En app/model/rest.py se definen los modelos que servirán para comunicarse
### con el front end (tanto los que se reciben como los que se devuelven)
################################################################################

from model.rest import (
    TestData,
    TestRequest,
    EmailRequest,
    TestResponse,
    EmailResponse,
    ProspectoRequest,
    ProspectoResponce
)

################################################################################
### Se pueden definir errores personalizados (ver la implementación en el
### archivo EntityNotFoundException) 
################################################################################
router = APIRouter(responses=HTTP_RESPONSES)


@router.post("/registrar_email", response_model=EmailResponse)
async def registrar_email(data: EmailRequest) ->EmailResponse:
    id_email = handler.registrar_email_prospecto(data.email)

    return EmailResponse(
        estatus = 200,
        mensaje = "El emailse registró con éxito",
        id_nuevo_email = id_email
    )

@router.post("/registrar_prospecto", response_model=ProspectoResponce)
async def registrar_prospecto(prospecto: ProspectoRequest) -> ProspectoResponce:
    id_email, id_prospecto = handler.registrar_prospecto_m(prospecto)
    return ProspectoResponce(
        estatus = 200,
        mensaje= "Prospecto registrado exitosamente",
        id_email = id_email,
        id_prospecto = id_prospecto
    )

