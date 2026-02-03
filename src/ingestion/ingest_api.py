import requests
import json
import os 
import datetime

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}]{message}")

def ingest_endpoint(endpoint,filename):
    url = f"https://fakestoreapi.com/{endpoint}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        path = f"data/raw/{filename}.json"
        with open(path,"w") as f:
            json.dump(data,f, indent=2) #O que e onde
        
        #log
        log(f"{filename} salvo com sucesso! {len(data)} registros.")
        
    except requests.RequestException as e:
        log(f"Erro ao consumir endpoint{endpoint}: {e}")
def main():
    os.makedirs("data/raw", exist_ok=True)
    endpoints = {
        "products":"products",
        "users":"users",
        "carts":"carts"
    }
    for filename, endpoints in endpoints.items():
        ingest_endpoint(endpoints,filename)

if __name__ == "__main__":
    main()



