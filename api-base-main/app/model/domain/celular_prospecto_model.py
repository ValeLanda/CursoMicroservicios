class CelularProspectoModel:
    def __init__(self):
        self.IdTelefono: int
        self.Telefono: str
        self.IdSolicitud: int


    def valida_celular(celular:str) -> bool:
        if len(celular) ==10:
            return True
        else:
            return False