from sqlalchemy.sql.sqltypes import Date

class ClienteModel:
    def __init__(self):
        self.IdCliente: int
        self.NumeroCliente: str
        self.Email: str
        self.PrimerNombre: str
        self.SegundoNombre: str
        self.ApellidoPaterno: str
        self.ApellidoMaterno: str
        self.CURP: str
        self.FechaNacimiento: Date
        self.Celular: str
        self.RFC: str