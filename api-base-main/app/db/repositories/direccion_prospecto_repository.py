from operator import imod
from typing import Any

from common.db.base import BaseRepository
from model.domain.direccion_prospecto_model import DireccionProspectoModel

class DireccionProspectoRepository(BaseRepository):
    def __init__(self,session) -> None:
        super().__init__()
        self.session = session

    def get(self, int:id) -> Any:
        return self.session.query(DireccionProspectoModel).filter_by(Id=id).first()

    def add(self, direccion_model):
        self.session.add(direccion_model)
        self.session.flush()
        self.session.refresh(direccion_model)