import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

CSV_FILE = 'taxa-cdi.csv'

# Verifica se o arquivo CSV existe antes de carregar
if not os.path.exists(CSV_FILE):
    print(f"❌ Erro: Arquivo '{CSV_FILE}' não encontrado.")
    sys.exit(1)

# Lê os dados do CSV
try:
    df = pd.read_csv(CSV_FILE)
except Exception as e:
    print(f"❌ Erro ao carregar o arquivo CSV: {e}")
    sys.exit(1)

# Verifica se as colunas necessárias estão no DataFrame
if 'hora' not in df.columns or 'taxa' not in df.columns:
    print("❌ Erro: O CSV não contém as colunas necessárias ('hora' e 'taxa').")
    sys.exit(1)

# Criando o gráfico
plt.figure(figsize=(10, 5))
grafico = sns.lineplot(x=df['hora'], y=df['taxa'])

# Garantindo que os ticks correspondam ao número correto de labels
ticks = range(len(df['hora']))
grafico.set_xticks(ticks)
grafico.set_xticklabels(df['hora'][:len(ticks)], rotation=90)

plt.xlabel("Hora")
plt.ylabel("Taxa CDI")
plt.title("Variação da Taxa CDI ao Longo do Tempo")

# Verifica se o nome do arquivo foi passado como argumento
if len(sys.argv) < 2:
    print("❌ Erro: Nome do arquivo de saída não fornecido.")
    sys.exit(1)

output_file = f"{sys.argv[1]}.png"
plt.savefig(output_file, bbox_inches='tight')  # Salva a imagem sem cortar rótulos
print(f"✅ Sucesso! Gráfico salvo como '{output_file}'.")
