from sqlalchemy.sql.sqltypes import Date

class ProspectoModel:
    def __init__(self):
        self.IdProspecto: int
        self.IdEmail: int
        self.IdEstatusSolicitud: int
        self.PrimerNombre: str
        self.SegundoNombre: str
        self.ApellidoPaterno: str
        self.ApellidoMaterno: str
        self.CURP: str
        self.FechaNacimiento: Date
        self.RFC: str