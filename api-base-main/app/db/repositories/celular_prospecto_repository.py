from operator import imod
from typing import Any

from common.db.base import BaseRepository
from model.domain.celular_prospecto_model import CelularProspectoModel


class CelularProspectoRepository(BaseRepository):
    def __init__(self,session) -> None:
        super().__init__()
        self.session = session

    def get(self, int:id) -> Any:
        return self.session.query(CelularProspectoModel).filter_by(Id=id).firts()

    def add(self, celular_prospecto):
        self.session.add(celular_prospecto)
        self.session.flush()
        self.session.refresh(celular_prospecto)