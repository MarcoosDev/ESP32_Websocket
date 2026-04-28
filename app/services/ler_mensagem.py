from fastapi import WebSocket
from app.models.clientes_model import Cliente
from app.services.actions import Action

async def ler_mensagem(payload, ws : WebSocket):
    cliente = Cliente(mensagem=payload)
    action = Action(
        cliente = cliente,
        ws = ws
        )
    
    match (cliente.tipo):
        case "send_api_key":
            return await action.receber_apikey(), cliente
        
        case "SendMensageExtern":
            return await action.enviar_mensagem_extern(), cliente
    