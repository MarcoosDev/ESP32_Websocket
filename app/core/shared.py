from fastapi import WebSocket
from app.core.database import DataBase
from app.models.valor import Val
from typing import Dict
import asyncio

database = DataBase()
valor = Val()
API_KEY = database.apy_key
SERVER_ID = database.internal_id
active_connections: Dict[str, WebSocket] = {}
active_connections_lock = asyncio.Lock()


