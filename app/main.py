from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from app.routes import dispositivos_router, mensagens_router
from app.core.shared import valor,active_connections_lock, active_connections
from app.services.ler_mensagem import ler_mensagem
from app.models.clientes_model import Cliente
import json

app = FastAPI(title="ESP32 servidor WebSocket ")

app.include_router(dispositivos_router)
app.include_router(mensagens_router)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Nova conexão recebida")
    try:
        device_id = None
        receber_api_key = await asyncio.wait_for(
            websocket.receive_text(),
            timeout=10.0  
        )
        receber_api_key = json.loads(receber_api_key)
        ws, clien = await ler_mensagem(payload = receber_api_key, websocket = websocket);
        if ws == valor.api_invalid:
            return
        device_id = clien.id
        while True:
            mensagem = await websocket.receive_text()
            mensagem = json.loads(mensagem)
            ws, clien = await ler_mensagem(payload = mensagem, websocket = websocket);
            if ws == valor.api_invalid:
                break
                    
    except asyncio.TimeoutError:
        print(f"Timeout na autenticação/registro para {device_id or 'novo cliente'}")
    except WebSocketDisconnect:
        print(f"{device_id if device_id else 'dispositivo'} desconectado")
    except Exception as e:
        print(f"Erro inesperado para {device_id or 'cliente'}: {e}")
    finally:
        if device_id and active_connections.get(device_id) == websocket:
            del active_connections[device_id]
            print(f"{device_id} removido! Total: {len(active_connections)}")



@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def health_check():
    return {"total": len(active_connections),"status": "ok"}