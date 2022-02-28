from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import errors
from pydantic.error_wrappers import ValidationError
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from model.errors import EntityNotFoundException
from model.errors import NotFoundMessage
from services import base_handler as handler
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
    TestResponse,
    DatosAlta,
)

################################################################################
### Se pueden definir errores personalizados (ver la implementación en el
### archivo EntityNotFoundException) 
################################################################################
router = APIRouter(responses=HTTP_RESPONSES)


################################################################################
### Se definen los parámetros que se reciben y los que se devuelven con base 
### en el modelo
################################################################################



@router.post("/test", response_model=TestResponse)
async def test(test_params: TestRequest) -> TestResponse:
    
    resp  = str(handler.consulta_retenido()) + " - " + str(handler.consulta_retenido_amex())

    return TestResponse(
        estatus = 1,
        mensaje = "OK",
        datos=TestData(
            valor1 = 100,
            valor2 = resp
        )
    )

@router.post("/add", response_model=TestResponse)
async def test(alta: DatosAlta) -> TestResponse:
    new_id = handler.agregar_registro(alta.nombre, alta.comentarios)

    return TestResponse(
        estatus = 1,
        mensaje = "OK",
        datos=TestData(
            valor1 = new_id,
            valor2 = "Valor dado de alta correctamente"
        )
    )

@router.get("/get", response_model=TestResponse)
async def test(id:int = 0, authorize: AuthJWT = Depends()) -> TestResponse:
    # descomentar la siguiente línea si se tiene implementado el API de autentificación
    # authorize.jwt_required()
    try:
        registro = handler.obtener_registro(id)
        
        if(not registro):
            # Se pueden generar nuestras propias excepciones para que devuelvan
            # un código expecífico, pero se tiene que especificar en el router
            # y en el main cómo se maneja
            raise EntityNotFoundException(description="El registro no existe")
    except Exception as e:
        logger.debug(repr(e))
        raise HTTPException(status_code=500, detail=str(e))

    return TestResponse(
        estatus = 1,
        mensaje = "OK",
        datos=TestData(
            valor1 = registro.Id,
            valor2 = registro.Mensaje
        )
    )

@router.post("/protected/{numCta}/", response_model=TestResponse)
async def protected(numCta:int, authorize: AuthJWT = Depends()) -> TestResponse:

    authorize.jwt_required()
    return handler.probar_http_session(token=authorize._token, num_cta=numCta)

