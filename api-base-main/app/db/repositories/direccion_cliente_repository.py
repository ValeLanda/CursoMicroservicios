from operator import imod
from typing import Any

from common.db.base import BaseRepository
from model.domain.direccion_cliente_model import DireccionClienteModel

class DireccionClienteRepository(BaseRepository):
    def __init__(self,session) -> None:
        super().__init__()
        self.session = session

    def get(self, int:id) -> Any:
        return self.session.query(DireccionClienteModel).filter_by(Id=id).first()

    def add(self, direccion_cliente):
        self.session.add(direccion_cliente)
        self.session.flush()
        self.session.refresh(direccion_cliente)