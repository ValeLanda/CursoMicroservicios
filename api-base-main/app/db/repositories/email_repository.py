from operator import imod
from typing import Any

from common.db.base import BaseRepository
from model.domain.email_model import EmailModel

class EmailRepository(BaseRepository):
    def __init__(self,session) -> None:
        super().__init__()
        self.session = session

    def get(self, int:id) -> Any:
        return self.session.query(EmailModel).filter_by(Id=id).first()

    def add(self, email_model):
        self.session.add(email_model)
        self.session.flush()
        self.session.refresh(email_model)

