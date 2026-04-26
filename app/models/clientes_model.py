import json

class Cliente:
    def __init__(self, mensagem):
        tipo = mensagem.get("type")
        origem = mensagem.get("origem")
        destinatario = mensagem.get("destinatario")
        msg = mensagem.get("mensagem")
        self.tipo = tipo
        self.origem = origem
        self.id = origem
        self.destin = destinatario
        self.mensagem = msg

        