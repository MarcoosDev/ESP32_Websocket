class Cliente:
    def __init__(self, msg : dict):
        self.tipo = msg.get("type")
        self.origem = msg.get("origem")
        self.id = self.origem
        self.destin = msg.get("destinatario")
        self.msg = msg.get("mensagem")