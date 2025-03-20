import gspread
from oauth2client.service_account import ServiceAccountCredentials

def salvar_no_sheets(nome, cpf, chamado, opcao):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("Chamados Cartório").sheet1
    sheet.append_row([nome, cpf, chamado, opcao])

# Exemplo de uso:
salvar_no_sheets("João Silva", "12345678900", "987654", "Solicitação de Certidão")
