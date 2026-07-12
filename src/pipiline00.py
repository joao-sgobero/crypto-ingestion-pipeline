import requests
from tinydb import TinyDB
from datetime import datetime
import time

#Extrair dados do valor do bitcoin
def extract_bitcoin_data():
    url = "https://api.coinbase.com/v2/prices/spot"
    
    response = requests.get(url)
    data = response.json()
    return data

#Transformando os dados
def transform_bitcoin_data(data):
    valor = data['data']['amount']
    criptomoeda = data['data']['base']
    moeda = data['data']['currency']
    timestamp = datetime.now().timestamp()
    
    transform_data = {
        "valor": valor,
        "criptomoeda": criptomoeda,
        "moeda": moeda,
        "timestamp": timestamp
    }
    
    return transform_data

#Carregar dados em um banco de dados
def load_bitcoin_tinydb(data, db_name="bitcoin_json"):
    db = TinyDB(db_name)
    db.insert(data)
    print("Carregamento realizado com sucesso.")


if __name__ == '__main__':
    while True:
        data = extract_bitcoin_data()
        transform_data = transform_bitcoin_data(data)
        load_bitcoin_tinydb(transform_data)
        time.sleep(12)