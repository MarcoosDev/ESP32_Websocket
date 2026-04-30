from fastapi import APIRouter

"""Principais rotas de comunicação entre usuarios externos e os clientes conectados"""
dispositivos_router = APIRouter(prefix="/api/dispositivos", tags=["Dispositivos"])
mensagens_router = APIRouter(prefix="/api/mensagens", tags=["Mensagens"])

from . import dispositivos
from . import mensagens