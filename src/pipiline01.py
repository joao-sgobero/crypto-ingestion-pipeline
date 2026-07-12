import requests
import psycopg2
import os
from dotenv import load_dotenv   #poetry add python-dotenv
from tinydb import TinyDB
from datetime import datetime
import time


# Carregar as configurações do arquivo .env
load_dotenv()


# Função para Extrair dados do valor do bitcoin
def extract_bitcoin_data():
    url = "https://api.coinbase.com/v2/prices/spot"
    
    response = requests.get(url)
    data = response.json()
    return data

# Função para Transformando os dados
def transform_bitcoin_data(data):
    valor = data['data']['amount']
    criptomoeda = data['data']['base']
    moeda = data['data']['currency']
    timestamp = datetime.now()
    
    transform_data = {
        "valor": valor,
        "criptomoeda": criptomoeda,
        "moeda": moeda,
        "timestamp": timestamp
    }
    
    return transform_data

# Função para criar tabela no banco de dados (Executado apenas uma vez)
def create_table():
    try:
        conn = psycopg2.connect(
            dbname = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            host = os.getenv("DB_HOST"),
            port = os.getenv("DB_PORT")
        )
        with conn.cursor() as cur:
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS bitcoin_table (
                            id SERIAL PRIMARY KEY,
                            valor NUMERIC NOT NULL,
                            criptomoeda VARCHAR(10) NOT NULL,
                            moeda VARCHAR(10) NOT NULL,
                            timestamp TIMESTAMP NOT NULL
                        )
                        """)
            conn.commit()
            print("Tabela criada e verificada com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        if conn:
            conn.close()
        


# Função para carregar dados no PostgreSQL
def load_bitcoin_postgres(data):
    try:
        conn = psycopg2.connect(
            dbname = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            host = os.getenv("DB_HOST"),
            port = os.getenv("DB_PORT")
        )
        with conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO bitcoin_table (valor, criptomoeda, moeda, timestamp)
                        VALUES (%s, %s, %s, %s)
                        """, (data['valor'], data['criptomoeda'], data['moeda'], data['timestamp'])
                        )
            conn.commit()
            print("Carregamento realizado com sucesso!")
    
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
    
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    #Criar a tabela para inicialização.
    create_table()
    
    try:
        #Loop principal
        while True:
            data = extract_bitcoin_data()
            transform_data = transform_bitcoin_data(data)
            load_bitcoin_postgres(transform_data)
            time.sleep(12)
    except KeyboardInterrupt:
        print("Execução foi interrompida pelo usuário.")
    