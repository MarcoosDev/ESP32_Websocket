import asyncio
from fastapi import WebSocket
from app.models.clientes_model import Cliente
from app.services.actions import Action

async def ler_mensagem(payload, websocket : WebSocket):
    cliente = Cliente(mensagem=payload)
    action = Action(
        cliente = cliente,
        ws = websocket
        )
    
    match (cliente.tipo):
        case "send_api_key":
            return await action.receber_apikey()
        
        case "SendMensageExtern":
            return await action.enviar_mensagem_extern()
    