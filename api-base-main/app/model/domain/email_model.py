from datetime import date
import re
from sqlalchemy.sql.sqltypes import Date

class EmailModel:
    def __init__(self):
        self.IdEmail: int
        self.Email: str


    def valida_email(self) -> bool:
        expresion_regular = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.match(expresion_regular, self.Email)):
            return True
        else:
            return False

    def email_valido(self) -> bool:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, self.Email)):
            return True
        else:
            return False


