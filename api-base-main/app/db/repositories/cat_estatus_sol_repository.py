from operator import imod
from typing import Any

from common.db.base import BaseRepository
from model.domain.cat_estatus_sol_model import CatEstatusSolicitudModel


class CatEstatusSolicitudRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__()

    def get(self, int:id) -> Any:
        return self.session.query(CatEstatusSolicitudModel).filter_by(Id=id).first()

    def add(self, cat_estatus_sol):
        self.session.add(cat_estatus_sol)