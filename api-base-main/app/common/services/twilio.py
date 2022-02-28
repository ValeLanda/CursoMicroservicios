from datetime import datetime
from twilio.rest import Client
from loguru import logger
from fastapi import HTTPException, status
from common.config import TWILIO_FROM_NUMBER, TWILIO_USER_NAME, TWILIO_USER_PWD

from services.messages import SYSTEM_EXCEPTION

def send_sms(numero_celular: str, message:str ):
    try:
        numero_destino ="+52"+str(numero_celular)
        client = Client(TWILIO_USER_NAME, TWILIO_USER_PWD)
        client.messages.create(to=numero_destino, from_=TWILIO_FROM_NUMBER, body=message)
    except Exception as err:
        logger.exception(str(datetime.datetime.now().date()) + " - " + str(datetime.datetime.now().time()) + ": " + str(err))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SYSTEM_EXCEPTION,
            headers={"WWW-Authenticate": "Bearer"},
        )
