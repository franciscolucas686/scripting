import os
import time
import json
import requests
from random import random
from datetime import datetime
from pathlib import Path

# URL correta para obter a taxa CDI do Banco Central
URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados?formato=json'
CSV_FILE = Path('taxa-cdi.csv')

def obter_taxa_cdi():
    """Obtém a taxa CDI da API do Banco Central e retorna como float."""
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        dados = response.json()

        if isinstance(dados, list) and len(dados) > 0 and 'valor' in dados[-1]:
            return float(dados[-1]['valor']) + (random() - 0.5)
        else:
            print("⚠️ Erro: Resposta inesperada da API", dados)
            return None
    except requests.exceptions.RequestException as e:
        print(f"🌐 Erro de conexão: {e}")
    except json.JSONDecodeError:
        print("⚠️ Erro ao decodificar JSON da resposta.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    return None

# Cria o arquivo CSV se não existir
if not CSV_FILE.exists():
    CSV_FILE.write_text('data,hora,taxa\n', encoding='utf8')

# Loop para capturar os dados 10 vezes
for _ in range(10):
    data_e_hora = datetime.now()
    data = data_e_hora.strftime('%Y/%m/%d')
    hora = data_e_hora.strftime('%H:%M:%S')

    cdi = obter_taxa_cdi()

    # Apenas grava se houver um valor válido
    if cdi is not None:
        with CSV_FILE.open('a', encoding='utf8') as fp:
            fp.write(f'{data},{hora},{cdi:.4f}\n')

    time.sleep(2 + (random() - 0.5))

print("✅ Sucesso! Dados extraídos.")
