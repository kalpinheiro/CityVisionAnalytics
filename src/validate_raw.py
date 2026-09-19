import pandas as pd

arquivo = "data/raw/nyc311_2026-01_2026-06.jsonl"

total_registros = 0
menor_data = None
maior_data = None
chaves = set()

for chunk in pd.read_json(arquivo, lines=True, chunksize=10000):
    total_registros += len(chunk)

    datas = pd.to_datetime(chunk["created_date"], errors="coerce")

    data_min = datas.min()
    data_max = datas.max()

    if menor_data is None or data_min < menor_data:
        menor_data = data_min

    if maior_data is None or data_max > maior_data:
        maior_data = data_max

    chaves.update(chunk["unique_key"])

print(f"Total de registros: {total_registros}")
print(f"Menor created_date: {menor_data}")
print(f"Maior created_date: {maior_data}")
print(f"Unique keys distintas: {len(chaves)}")
print(f"Possíveis duplicatas: {total_registros - len(chaves)}")