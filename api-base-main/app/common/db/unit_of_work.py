import abc
import random
import string
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger
from common.config import HOST, PORT, USER, PWD, DB

_str_url = f'mysql+mysqldb://{USER}:{PWD}@{HOST}:{PORT}/{DB}?charset=utf8'
_isolation_level="REPEATABLE READ"

DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        _str_url,
        isolation_level=_isolation_level,
        pool_recycle=3600,
        connect_args={'connect_timeout': 8},
    )
)

class AbstractUnitOfWork(abc.ABC):

    @abc.abstractmethod
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.session.close()

    @abc.abstractmethod
    def commit(self):
        self.session.commit()

    @abc.abstractmethod
    def rollback(self):
        self.session.rollback()
