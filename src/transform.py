import pandas as pd

arquivo = "data/raw/nyc311_2026-01_2026-06.jsonl"

colunas = [
    "unique_key",
    "created_date",
    "closed_date",
    "status",
    "agency",
    "agency_name",
    "complaint_type",
    "descriptor",
    "location_type",
    "borough",
    "city",
    "community_board"
]

colunas_texto = [
    "status",
    "agency",
    "agency_name",
    "complaint_type",
    "descriptor",
    "location_type",
    "borough",
    "city",
    "community_board"
]


def transformar_dados(arquivo, tamanho_chunk=10000):
    for chunk in pd.read_json(
        arquivo,
        lines=True,
        chunksize=tamanho_chunk
    ):
        chunk = chunk[colunas]

        for coluna in colunas_texto:
            chunk[coluna] = chunk[coluna].str.strip()

        chunk["created_date"] = pd.to_datetime(
            chunk["created_date"],
            errors="coerce"
        )

        chunk["closed_date"] = pd.to_datetime(
            chunk["closed_date"],
            errors="coerce"
        )

        chunk = chunk[
            chunk["closed_date"].isna()
            | (chunk["closed_date"] >= chunk["created_date"])
        ].copy()

        chunk["resolution_time_seconds"] = (
            chunk["closed_date"] - chunk["created_date"]
        ).dt.total_seconds().round().astype("Int64")

        yield chunk


