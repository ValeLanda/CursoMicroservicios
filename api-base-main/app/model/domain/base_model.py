from datetime import date

from sqlalchemy.sql.sqltypes import Date
class BaseModel:
    def __init__(self):
        self.Id: int
        self.FechaReporte: Date
        self.CodigoClave:int
        self.TipoInstitucion: str
        self.Mensaje:str
        self.FacebookId: str
        self.Respuesta: int



