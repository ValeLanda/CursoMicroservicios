from fastapi import APIRouter

from routes import controller
from routes import solicitud

api_router = APIRouter()
api_router.include_router(controller.router, tags=["pruebas"], prefix="/base")
api_router.include_router(solicitud.router, tags=["solicitud"], prefix="/solicitud")