from operator import ne
from typing import Any

from sqlalchemy.sql.sqltypes import Date
from db.demo_uow import SqlAlchemyUnitOfWork

from datetime import date
from model.domain.base_model import BaseModel

import requests

from model.rest import TestData, TestResponse

HTTP_SESSION = requests.Session()

def probar_http_session(token: str, num_cta:str) -> TestResponse:
    head = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}
    req = requests.Request('GET',  f"https://apim.perfekti.mx/v1/cuentas/{num_cta}/saldos/",
        headers=head
    )
    prepped = HTTP_SESSION.prepare_request(req)
    resp = HTTP_SESSION.send(prepped)

    response = TestResponse(
        estatus = resp.status_code,
        mensaje = "OK",
        datos = TestData(
            valor1 = 1,
            valor2 = "Nada"
        ),
    )
    return response

def agregar_registro(nombre: str, mensaje: str)->int:
    with SqlAlchemyUnitOfWork() as uow:
        new_model = BaseModel()
        new_model.FechaReporte = date.today()
        new_model.CodigoClave = 2
        new_model.TipoInstitucion = nombre
        new_model.Mensaje = mensaje
        new_model.FacebookId  = "10154509875362000"
        new_model.Respuesta = 23
        uow.base_repository.add(new_model)
        uow.commit()
    return new_model.Id

def obtener_registro(id: int) -> BaseModel:
    with SqlAlchemyUnitOfWork() as uow:
        return uow.base_repository.get(id)

def consulta_retenido() -> Any:
    with SqlAlchemyUnitOfWork() as uow:
        return uow.base_repository.obtener_suma_movimientos_pendientes(89596)

def consulta_retenido_amex() -> Any:
    with SqlAlchemyUnitOfWork() as uow:
        return uow.base_repository.obtener_suma_movimientos_pendientes_amex(89596)
