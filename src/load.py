from sqlalchemy import create_engine
from transform import transformar_dados

server = r"localhost\SQLEXPRESS"
database = "CityVisionAnalytics"

connection_string = (
    "mssql+pyodbc://"
    f"{server}/{database}"
    "?trusted_connection=yes"
    "&driver=ODBC+Driver+17+for+SQL+Server"
)

engine = create_engine(connection_string)

def carregar_chunk(chunk, engine):
    chunk.to_sql(
        name="stg_nyc311",
        con=engine, 
        schema="dbo", 
        if_exists="append", 
        index = False,
        chunksize=2000
    )

for chunk in transformar_dados("data/raw/nyc311_2026-01_2026-06.jsonl"):
    print(f"Carregando chunk com {len(chunk)} registros...")
    carregar_chunk(chunk, engine)
    print("Chunk carregado com sucesso!")
