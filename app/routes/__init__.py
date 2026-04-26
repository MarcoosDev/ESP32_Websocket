from fastapi import APIRouter

dispositivos_router = APIRouter(prefix="/api/dispositivos", tags=["Dispositivos"])
mensagens_router = APIRouter(prefix="/api/mensagens", tags=["Mensagens"])

from . import dispositivos
from . import mensagens