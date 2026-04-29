from app.core.database import DataBase
from app.core.shared import active_connections
from app.routes import mensagens_router as router
from app.models.json_model import Json_format
json = Json_format()
database = DataBase()
API_KEY = database.apy_key

@router.post("/enviar/{nome}/{texto}")
async def enviar_para_dispositivo(nome: str, texto: str, data: dict):
    api_key = data.get("api_key")
    
    if api_key != API_KEY:
        return {"status": 401, "erro": "API key inválida"}

    if not active_connections:
        return{"status": 400, "erro": "Nenhum dispositivo conectado"}
    
    if nome not in active_connections:
        return {
            "status": 404,
            "erro": f"Dispositivo '{nome}' não encontrado",
            "disponiveis": list(active_connections.keys())
        }
    
    await json._enviar_json (
            tipo=database.extern_id,
            origem=database.extern_id,
            destinatario = nome,
            mensagem=texto,
            websocket= active_connections[nome]
        )
    return {
        "status": 200,
        "dispositivo": nome,
        "mensagem": texto
    }


@router.post("/enviar_all/{texto}")
async def enviar_para_todos(texto: str, data: dict):
    api_key = data.get("api_key")

    if api_key != API_KEY:
        return {"status": 401, "erro": "API key inválida"}
    
    if not active_connections:
        return {"status": 400, "erro": "Nenhum dispositivo conectado"}

    sucessos = []
    for nome, conexao in active_connections.items():
        try:
            await json._enviar_json(
            tipo = database.extern_id,
            origem = database.extern_id,
            destinatario = nome,
            mensagem = texto,
            websocket = conexao
            )
            sucessos.append(nome)
            
        except:
            print(f"Falha ao enviar para {nome}")

    return {
        "status": 200,
        "mensagem": texto,
        "enviado_para": sucessos,
        "total": len(sucessos)
    }

    
