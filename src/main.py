import requests

url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"

resposta = requests.post(url, timeout=10)

print(resposta.status_code)
print(resposta.text)