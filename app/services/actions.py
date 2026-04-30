from app.core.shared import active_connections, active_connections_lock,API_KEY, SERVER_ID, valor
from app.models.clientes_model import Cliente
from app.models.json_model import Json_format
from fastapi import WebSocket

class Action:
    def __init__(self, cliente: Cliente, ws: WebSocket):
        self.cliente = cliente
        self.websocket = ws
        self.json = Json_format(
            websocket=ws, 
            cliente=cliente
        )


    async def receber_apikey(self):
        """
        recebe a chave api, se valida, salva o id do cliente
        presente em "origem" no json recebido. Se a chave api for
        invalida, fecha a conexão automaticamente
        """
        
        if self.cliente.mensagem != API_KEY:

            await self.json._enviar_json(
                tipo=valor.response_server,
                origem=SERVER_ID,
                destinatario=self.cliente.origem,
                mensagem=valor.api_invalid
            )

            await self.websocket.close()

            return valor.api_invalid

        await self.receber_id()
        
        await self.json._enviar_resposta(
            mensagem=valor.conn_concluita,
            destinatario=self.cliente.origem
        )
        print("Cliente autenticado com sucesso!")
        

    async def receber_id(self):
        """"
        def para organizar ID do usuario e salvar na lista
        futuramente irei colocar um db para salvar os clientes conectados
        """
        device_id = self.cliente.origem

        if not device_id or len(device_id) > 100:  
            await self.json._enviar_erro(mensagem = valor.id_invalid, destinatario=self.cliente.id)
            await self.websocket.close()
            return

        async with active_connections_lock:
            old_ws = active_connections.pop(device_id, None)
            active_connections[device_id] = self.websocket

        if old_ws is not None:
            try:
                await old_ws.close(code=1000, reason="Nova conexão")
            except Exception:
                pass
            
        total_conns = len(active_connections)
        print(f"{device_id} registrado! Total: {total_conns}")


    async def enviar_mensagem_extern(self):
        """
        envia mensagens entre clientes, realizando a função
        principal do projeto, que é ser uma ponte entre dois ou mais dispotivos com websocket
        """

        codigo_websocket = None

        async with active_connections_lock:
            codigo_websocket = active_connections.get(self.cliente.destin)

        if codigo_websocket:
            print(f"Encontrado! Destino: {self.cliente.destin}")

            try:
                await self.json._enviar_json(
                    tipo=valor.mensagem_externa,
                    origem=self.cliente.id,
                    destinatario=self.cliente.destin,
                    mensagem=self.cliente.mensagem,
                    websocket=codigo_websocket
                )

                print("Envio Concluído com sucesso!")

            except Exception as e:
                print(f"Falha ao enviar para {self.cliente.destin}: {e}")
                async with active_connections_lock:
                    chave_para_remover = next(
                        (chave for chave, ws in active_connections.items() 
                        if ws == codigo_websocket), 
                        None
                    )
                    if chave_para_remover is not None:
                        del active_connections[chave_para_remover]

        else:
            await self.json._enviar_erro(
                mensagem=valor.destinatario_invalido,
                destinatario=self.cliente.id
            )
            print(f"{self.cliente.destin} não encontrado em nenhuma chave")


    async def enviar_extern_all(self):
        """envia mensagens a todos os clientes conectados,
        menos o proprio que solicitou o envio"""

        if len(active_connections) < 2:
            await self.json._enviar_erro(
                mensagem = valor.sem_clientes,
                destinatario = self.cliente.id
            )

        async with active_connections_lock:
            for chave, ws in list(active_connections.items()):
                if chave != self.cliente.id:
                    await self.json._enviar_json(
                        tipo = valor.mensagem_externa,
                        origem = self.cliente.id,
                        destinatario = chave,
                        mensagem = self.cliente.mensagem,
                        websocket = ws,
                    )