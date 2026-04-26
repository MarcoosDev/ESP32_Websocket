# 🌐 ESP32_Websocket Hub

> [!IMPORTANT]
> **Status: Em Desenvolvimento** 🚀
> 
> Este projeto está sendo desenvolvido desde **18/04/2026** e está sujeito a alterações e melhorias.
> Documentando minha jornada de aprendizado e desenvolvimento.

---

## 📊 Badges do Projeto

[![Platform: ESP32](https://img.shields.io/badge/Platform-ESP32-blue)]()
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136.0-009688?logo=fastapi&logoColor=white)
![WebSockets](https://img.shields.io/badge/WebSockets-16.0-010101?logo=socket.io&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-0.44.0-499848?logo=uvicorn&logoColor=white)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/seuusuario/ESP32_Websocket_Hub/actions)

---

## 📖 O Que é Este Projeto?

### O Problema
Trabalhar com dispositivos IoT (ESP32, ESP8266, Arduinos) é complexo:
- ❌ Gerenciar comunicação com servidor central
- ❌ Lidar com firewalls e NAT
- ❌ Resolver IPs dinâmicos
- ❌ Tratamento de reconexões
- ❌ Problemas de latência

### A Solução
**ESP32_Websocket Hub** cria uma **ponte transparente** entre seus dispositivos e qualquer servidor backend, oferecendo:
- ✅ WebSockets para comunicação bidirecional em tempo real
- ✅ Baixo overhead de processamento
- ✅ Alta confiabilidade e estabilidade
- ✅ Portal web para monitoramento
- ✅ Ideal para prototipagem rápida

---

## ⚡ Funcionalidades Principais

| Funcionalidade | Descrição |
|---|---|
| 🔌 **Ponte WebSocket** | Comunicação bidirecional em tempo real |
| 🔐 **Autenticação Segura** | Handshake em 3 etapas com API_KEY |
| 📱 **Multi-Dispositivos** | Gerencia múltiplos ESP32/Arduino |
| 🔄 **Atualização OTA** | Firmware update via ponte |
| 🔗 **API REST** | Endpoints para status e mensagens |

---

## Pré-requisitos

### Hardware Necessário
- **Servidor**: Computador (Windows, macOS ou Linux)
- **Clientes**: ESP32, ESP8266 ou Arduino com WiFi

### Software Necessário
    Python 3.11 ou superior
    FastAPI, Uvicorn, WebSockets (via pip)
    Arduino IDE + biblioteca WebSocketsClient
    Acesso à rede WiF

---

## Instalação Passo a Passo

1. Clone o Repositório
   ```
   git clone https://github.com/MarcoosDev/ESP32_Websocket.git
   cd ESP32_Websocket_Hub
   ```

2. Instale as dependências Python:
   ```
   pip install fastapi uvicorn websockets
   ```

3. Para o lado ESP32: Instale a biblioteca WebSocketsClient no Arduino IDE via Library Manager.

4. Execute o servidor:
   ```
   uvicorn main:app --host 0.0.0.0 --port 3000 --reload
   ```

## Configuração

1. Defina a API_KEY no código do servidor (e.g., em `app/core/database.py`):
   ```python
   API_KEY = "minha_chave_secreta_123"
   ```
   Dica: Para produção, use variáveis de ambiente (.env)

2. Configure o IP e porta do servidor no código ESP32 
      ```
      const char* ws_host = "192.168.x.x";    // IP do seu servidor
      const uint16_t ws_port = 10000;           // Porta do servidor
      const char* ws_path = "/ws";             // Caminho WebSocket
      ```

3. Ajustes de segurança: Use HTTPS/WSS em produção e armazene API_KEY em variáveis de ambiente.

## Uso

1. Inicie o servidor backend com Uvicorn.

2. Faça upload do código ESP32 para o dispositivo.

3. O dispositivo se conectará automaticamente via WebSocket.

4. Envie mensagens via API para monitorar dispositivos ou enviar mensagens (e.g., com Postman).

5. Exemplos de uso:
   - Envie uma mensagem: 
      ```
      POST /api/mensagens/enviar/id_do_cliente/Hello com header: {"api_key": "Sua_chave_api"}
      ```
   - Liste dispositivos: 
      ```
      POST /api/dispositivos/list
      com header: {"api_key": "Sua_chave_api"}
      ```

**Nota**: O servidor mantém o estado mesmo após reconexões de dispositivos (ex: reinício do ESP32). Verifique os logs para debug.

## Estrutura do Projeto

```
ESP32_Websocket_Hub/
|
├── app/
|    ├── core/
|    |    ├── __init__.py  
|    |    ├── config.py
|    |    ├── database.py
|    |    └── shared.py
|    |
|    ├── models/
|    |    ├── __init__.py  
|    |    ├── clientes_model.py
|    |    ├── json_model.py
|    |    └── valor.py
|    |
|    ├── routes/
|    |    ├── __init__.py 
|    |    ├── dispositivos.py
|    |    └── mensagens.py
|    |
|    ├── services/
|    |    ├── __init__.py 
|    |    ├── actions.py
|    |    └── ler_mensagem.py
|    |    
|    ├── __init__.py 
|    └── main.py 
|
├── run.py
├── requirements.txt     
└── README.md            
```

## Modelo de Mensagem JSON

```text
{
  "type": "(send_api_key") or ("SendMensageExtern")",
  "origem": "Nome_do_seu_esp32 ou cliente",
  "destinatario": "SERVER_CENTRAL -> nome padrão desse servidor, pode ser mudado em databse.py",
  "mensagem": "Temperatura atual: 24.5°C" -> ou chave api, se for a primeira conexão
}
```
## Codigo exemplo ESP32

```text
#include <WiFi.h>
#include <WebSocketsClient.h>

const char* ssid = "NOME_DA_REDE";
const char* password = "SENHA_DA_REDE";

const char* ws_host = "192.168.x.xxx";  
const uint16_t ws_port = 10000;          
const char* ws_path = "/ws";              

WebSocketsClient webSocket;

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch (type) {
    case WStype_DISCONNECTED:
      Serial.println("[WS] Desconectado!");
      break;
    case WStype_CONNECTED: //somente nesse momento deve ser enviado a chave api
      Serial.println("[WS] Conectado ao servidor!");
      String jsonMsg = "{\"type\":\"tipo_da_mensagem\",\"origem\":\"nome_do_esp\",\"destinatario\":\"SERVER_CENTRAL\",\"mensagem\":\"a_mesma_api_do_servidor\"}";
      webSocket.sendTXT(jsonMsg);
      Serial.println("[WS] Mensagem enviada: " + jsonMsg);
      break;
    case WStype_TEXT:
      //o servidor retorna "conn.concluido" quando a conexão foi autorizada, confira outros retornos possiveis em "app/models/valor.py" 
      Serial.printf("[WS] Mensagem recebida: %s\n", payload);
      break;
    case WStype_ERROR:
      Serial.println("[WS] Erro!");
      break;
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("\nIniciando...");

  WiFi.begin(ssid, password);
  Serial.print("Conectando ao WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado!");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());

  webSocket.begin(ws_host, ws_port, ws_path);
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000); 
}

void loop() {
  webSocket.loop();
}
```

## Contato e Agradecimento

Para dúvidas ou sugestões, entre em contato:
- **Email**: marcosdevphb@gmail.com

