from operator import imod
from typing import Any
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql import select, and_

from common.db.base import BaseRepository
from model.domain.prospecto_model import ProspectoModel

class ProspectoRepository(BaseRepository):
    def __init__(self, session) -> None:
        super().__init__()
        self.session = session
    
    def get(self, id:int) -> Any:
        return self.session.query(ProspectoModel).filter_by(Id=id).first()

    def add(self, prospecto_model):
        self.session.add(prospecto_model)
        self.session.flush()
        self.session.refresh(prospecto_model)

