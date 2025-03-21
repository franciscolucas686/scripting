import os
import time
import json
import sys
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from random import random
from datetime import datetime

# URL da API do Banco Central
URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados?formato=json'


def extrair_dados(csv_filename="taxa-cdi.csv"):
    """Extrai os dados da API e salva no arquivo CSV."""
    for _ in range(10):
        data_e_hora = datetime.now()
        data = data_e_hora.strftime('%Y/%m/%d')
        hora = data_e_hora.strftime('%H:%M:%S')

        try:
            response = requests.get(URL)
            response.raise_for_status()
            dados = json.loads(response.text)

            if dados:
                ultimo_dado = dados[-1]  # Pega o último valor da API
                cdi = float(ultimo_dado['valor']) + (random() - 0.5)
            else:
                raise ValueError("Nenhum dado encontrado na API.")

        except (requests.RequestException, ValueError) as e:
            print(f"Erro ao obter dados: {e}")
            cdi = None

        # Criar o arquivo CSV caso não exista
        if not os.path.exists(csv_filename):
            with open(csv_filename, "w", encoding="utf8") as fp:
                fp.write("data,hora,taxa\n")

        # Salvar os dados no arquivo CSV
        with open(csv_filename, "a", encoding="utf8") as fp:
            fp.write(f"{data},{hora},{cdi}\n")

        time.sleep(2 + (random() - 0.5))

    print(f"Sucesso! Dados extraídos e salvos em {csv_filename}")


def gerar_grafico(csv_filename="taxa-cdi.csv", output_filename="grafico.png"):
    """Gera um gráfico da taxa CDI e salva como imagem."""
    try:
        df = pd.read_csv(csv_filename)

        plt.figure(figsize=(10, 5))
        grafico = sns.lineplot(x=df['hora'], y=df['taxa'])

        # Ajustando os ticks do eixo X antes de definir os rótulos
        grafico.set_xticks(range(len(df['hora'])))
        grafico.set_xticklabels(labels=df['hora'], rotation=90)

        plt.savefig(output_filename)
        print(f"Gráfico salvo como {output_filename}")

    except Exception as e:
        print(f"Erro ao gerar gráfico: {e}")


if __name__ == "__main__":
    # Nome do arquivo do gráfico passado como argumento
    output_filename = sys.argv[1] if len(sys.argv) > 1 else "grafico.png"

    # Executar os processos de extração e visualização
    extrair_dados()
    gerar_grafico(output_filename=output_filename)
