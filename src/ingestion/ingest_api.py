import requests
import json
import os
import datetime
import pandas as pd
from psycopg2 import sql
from src.config.database import get_connection

# =========================
# CONFIGURAÇÃO
# =========================
BASE_URL = "https://fakestoreapi.com"
# =========================
# LOG
# =========================

def log(message: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

# =========================
# INGESTÃO API
# =========================

def ingest_endpoint(endpoint: str, file_path: str):
    url = f"{BASE_URL}/{endpoint}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        log(f"{endpoint}: {len(data)} registros salvos em {file_path}")

    except requests.RequestException as e:
        log(f"Erro ao consumir endpoint {endpoint}: {e}")
        raise


# =========================
# PARQUET
# =========================

def save_as_parquet(file_path_json: str):
    df = pd.read_json(file_path_json)
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]

    file_path_parquet = file_path_json.replace(".json", ".parquet")
    df.to_parquet(file_path_parquet, index=False)

    log(f"Arquivo Parquet gerado: {file_path_parquet}")


# =========================
# LOAD POSTGRES
# =========================
def load_json_to_postgres(file_path: str, table_name: str):
    with get_connection() as conn:
        with conn.cursor() as cursor:

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            query = sql.SQL("""
                INSERT INTO staging.{} (payload)
                VALUES (%s)
            """).format(sql.Identifier(table_name))

            for record in data:
                cursor.execute(query, (json.dumps(record),))

            log(f"{len(data)} registros inseridos em staging.{table_name}")


# =========================
# TESTE CONEXÃO
# =========================

def test_connection():
    try:
        with get_connection() as conn:
            log("Conexão com PostgreSQL bem sucedida!")
    except Exception as e:
        log(f"Erro ao conectar no PostgreSQL: {e}")
        raise


# =========================
# MAIN
# =========================

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw", "fakestore")
    os.makedirs(raw_dir, exist_ok=True)

    execution_timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    endpoints = ["products", "users", "carts"]

    test_connection()

    for endpoint in endpoints:
        file_name = f"{endpoint}_{execution_timestamp}.json"
        file_path = os.path.join(raw_dir, file_name)

        ingest_endpoint(endpoint, file_path)
        save_as_parquet(file_path)
        load_json_to_postgres(file_path, f"{endpoint}_raw")


if __name__ == "__main__":
    main()
