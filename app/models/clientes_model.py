class Cliente:
    def __init__(self, mensagem):
        self.tipo = mensagem.get("type")
        self.origem = mensagem.get("origem")
        self.id = self.origem
        self.destin = mensagem.get("destinatario")
        self.mensagem = mensagem.get("mensagem")