from operator import imod
from typing import Any
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql import select, and_

from common.db.base import BaseRepository
from model.domain.base_model import BaseModel

class DemoRepository(BaseRepository):
    def __init__(self, session) -> None:
        super().__init__()
        self.session = session

    def get(self, id: int) -> Any:
        return self.session.query(BaseModel).filter_by(Id=id).first()
        
    def add(self, base_model):
        self.session.add(base_model)

    def obtener_suma_movimientos_pendientes_amex(self, num_cta: int):
        """
        @summary: Obtienen la suma de movimientos pendientes asociados a una cuenta
        @param Número de cuenta (int): Número de cuenta
        @return: suma de los movimientos pendientes
        """
        conn = self.session.connection().connection
        cursor = conn.cursor()
        cursor.callproc("sp_SumaMovPendientesAmex", [num_cta])
        result = list(cursor.fetchall())
        cursor.close()
        return result[0][0]

    def obtener_suma_movimientos_pendientes(self, num_cta: int):
        """
        @summary: Obtienen la suma de movimientos pendientes asociados a una cuenta
        @param Número de cuenta (int): Número de cuenta
        @return: suma de los movimientos pendientes
        """
        conn = self.session.connection().connection
        cursor = conn.cursor()
        cursor.callproc("sp_SumaMovPendientes", [num_cta])
        result = list(cursor.fetchall())
        cursor.close()
        return result[0][0]        

