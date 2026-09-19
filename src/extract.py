import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Autenticação
token = os.getenv("NYC_APP_TOKEN")
headers = {
    "X-App-Token": token
}

url = "https://data.cityofnewyork.us/api/v3/views/erm2-nwe9/query.json"

# Consulta à API
def extrair_dados(data_inicio, data_final):
    pagina = 645
    page_size = 1000

    while True: 
        dados = {
            "query": f"""
                SELECT *
                WHERE created_date >= '{data_inicio}'
                AND created_date < '{data_final}'
                ORDER BY created_date, unique_key
            """,
            "page": {
                "pageNumber": pagina,
                "pageSize": page_size
            }
        }

        tentativas = 3
        for tentativa in range(1, tentativas + 1):
            try:
                resposta = requests.post(url, headers=headers, json=dados, timeout=60)
                # Interrompe a execução caso a API retorne um erro HTTP
                resposta.raise_for_status()
                break
            except requests.exceptions.RequestException as erro:
                print(f"Erro na página {pagina}, tentativa {tentativa}/{tentativas}: {erro}")

                if tentativa == tentativas:
                    raise

        dados_api = resposta.json()
        with open("data/raw/nyc311_2026-01_2026-06.jsonl", "a", encoding="utf-8") as arquivo:
            for registro in dados_api:
                json.dump(registro, arquivo, ensure_ascii=False)
                arquivo.write("\n")

        quantidade = len(dados_api)
        print(f"Página {pagina}: {quantidade} registros")
        if quantidade < page_size:
            break
        else:
            pagina+=1   

extrair_dados("2026-01-01T00:00:00", "2026-07-01T00:00:00")







