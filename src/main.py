import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

url = "https://data.cityofnewyork.us/api/v3/views/erm2-nwe9/query.json"

# Autenticação
token = os.getenv("NYC_APP_TOKEN")

headers = {
    "X-App-Token": token
}

pagina = 1
page_size = 1000
todos_dados = []

while True:
    dados = {
        "query": "SELECT * WHERE created_date >= '2026-01-01'",
        "page": {
            "pageNumber": pagina,
            "pageSize": page_size
        }
    }

    # Consulta à API
    resposta = requests.post(
        url,
        headers=headers,
        json=dados,
        timeout=10
    )

    # Interrompe a execução caso a API retorne um erro HTTP
    resposta.raise_for_status()

    # Conversão da resposta JSON para estruturas Python
    dados_api = resposta.json()

    # Acumula os registros de todas as páginas
    todos_dados.extend(dados_api)

    quantidade = len(dados_api)

    print(f"Página {pagina}: {quantidade} registros")

    # Se a página não estiver cheia, chegamos ao final
    if quantidade < page_size:
        break

    pagina += 1

# Salva a resposta bruta da API para preservar os dados antes do tratamento
with open("data/raw/nyc311.json", "w", encoding="utf-8") as arquivo:
    json.dump(todos_dados, arquivo, ensure_ascii=False, indent=4)

print(f"Total de registros coletados: {len(todos_dados)}")
