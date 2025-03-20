from flask import Flask, request
import requests
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Token do WhatsApp API e número de telefone do bot
TOKEN = "SEU_TOKEN_DO_META"
PHONE_NUMBER_ID = "SEU_PHONE_NUMBER_ID"

# Função para enviar mensagem no WhatsApp
def enviar_mensagem(numero, mensagem):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": mensagem}
    }
    requests.post(url, json=payload, headers=headers)

# Webhook para receber mensagens
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if "messages" in data["entry"][0]["changes"][0]["value"]:
        mensagem = data["entry"][0]["changes"][0]["value"]["messages"][0]
        numero = mensagem["from"]
        texto = mensagem["text"]["body"]

        if "Bem-vindo" in texto:
            enviar_mensagem(numero, "Digite seu nome para prosseguirmos:")
        elif len(texto.split()) == 1:
            enviar_mensagem(numero, f"{texto}, agora informe seu CPF:")
        elif texto.isdigit():
            chamado = random.randint(100000, 999999)
            enviar_mensagem(numero, f"Certo, seu chamado é {chamado}. Escolha uma opção:\n1️⃣ Solicitar Certidão\n2️⃣ Protocolar Documentação\n3️⃣ Falar com um atendente")

    return "OK", 200

def salvar_no_sheets(nome, cpf, chamado, opcao):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("Chamados Cartório").sheet1
    sheet.append_row([nome, cpf, chamado, opcao])

# Exemplo de uso:
salvar_no_sheets("João Silva", "12345678900", "987654", "Solicitação de Certidão")

# Webhook para validar a URL no Meta for Developers
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == "SUA_CHAVE_DE_VERIFICACAO":
        return challenge
    return "Erro", 403

if __name__ == "__main__":
    app.run(port=5000)
