import requests
import json
import os
import datetime

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def ingest_endpoint(endpoint, file_path):
    url = f"https://fakestoreapi.com/{endpoint}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

        log(f"{file_path} salvo com sucesso! {len(data)} registros.")

    except requests.RequestException as e:
        log(f"Erro ao consumir endpoint {endpoint}: {e}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw", "fakestore")
    os.makedirs(raw_dir, exist_ok=True)

    execution_timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    endpoints = ["products", "users", "carts"]

    for endpoint in endpoints:
        file_name = f"{endpoint}_{execution_timestamp}.json"
        file_path = os.path.join(raw_dir, file_name)
        ingest_endpoint(endpoint, file_path)

if __name__ == "__main__":
    main()
