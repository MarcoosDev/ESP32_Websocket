from app.core.shared import  SERVER_ID, valor
import json

class Json_format:
    def __init__(self, websocket=None, cliente=None):
        self.websocket = websocket
        self.cliente = cliente
    

    def set_context(self, websocket=None, cliente=None):
        if websocket:
            self.websocket = websocket
        if cliente:
            self.cliente = cliente
    

    def _criar_json(self, tipo, origem, destinatario, mensagem):
        return json.dumps({
            "type": tipo,
            "origem": origem,
            "destinatario": destinatario,
            "mensagem": mensagem
        })
    

    async def _enviar_json(self, tipo, origem, destinatario, mensagem, websocket=None):
        json_str = self._criar_json(tipo, origem, destinatario, mensagem)
        ws = websocket or self.websocket
        
        if ws is None:
            raise ValueError("Nenhum WebSocket definido para envio")
        
        print(f"Enviando: {json_str}")
        await ws.send_text(json_str)
        return json_str


    async def _enviar_erro(self, mensagem, destinatario=None, websocket=None):
        dest = destinatario or (self.cliente.id if self.cliente else "unknown")
        return await self._enviar_json(
            tipo=valor.erro,
            origem=SERVER_ID,
            destinatario=dest,
            mensagem=mensagem,
            websocket=websocket
        )


    async def _enviar_resposta(self, mensagem, destinatario=None, websocket=None):
        dest = destinatario or (self.cliente.id if self.cliente else "unknown")
        return await self._enviar_json(
            tipo=valor.response_server,
            origem=SERVER_ID,
            destinatario=dest,
            mensagem=mensagem,
            websocket=websocket
        )