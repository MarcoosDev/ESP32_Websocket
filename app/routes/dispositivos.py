from fastapi import APIRouter
from app.core.shared import active_connections
from app.core.database import DataBase
from app.routes import dispositivos_router as router

database = DataBase()
API_KEY = database.apy_key

@router.post("/status")
async def status(data: dict):
    api_key = data.get("api_key")
    if api_key == API_KEY:
        return {
            "conectados": len(active_connections),
            "online": len(active_connections) > 0,
            "dispositivos": list(active_connections.keys())
        }
    else:
        return {"status": 401, "erro": "API key inválida"}

@router.post("/list")
async def listar_dispositivos(data : dict):
    api_key = data.get("api_key")
    if api_key == API_KEY:
        info = []
        for i, (device_id, ws) in enumerate(active_connections.items()):
            cliente_info = "desconhecido"
            if hasattr(ws, 'client') and ws.client:
                cliente_info = f"{ws.client[0]}:{ws.client[1]}"
            
            info.append({
                "id": i + 1,
                "nome": device_id,
                "cliente": cliente_info,
                "status": "conectado"
            })
        
        return {
            "total": len(active_connections),
            "dispositivos": info
        }
    else:
        return {"status": 401, "erro": "API key inválida"}
    


@router.get("/health")
async def health_check():
    return {"total": len(active_connections),"status": "ok"}
