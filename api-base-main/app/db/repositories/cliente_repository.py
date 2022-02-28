from operator import imod
from typing import Any

from common.db.base import BaseRepository
from model.domain.cliente_model import ClienteModel

class ClienteRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__()

    def get(self, int:id) -> Any:
        return self.session.query(ClienteModel).filter_by(Id=id).first()

    def add(self, cliente_model):
        self.session.add(cliente_model)