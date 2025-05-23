import pandas as pd
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
import random
import time
from itertools import combinations
import joblib

def carregar_e_preprocessar_dados(caminho_arquivo: str, nome_planilha: str, tamanho_amostra: int = None) -> tuple:
    """Carregar e preprocessar os dados de um arquivo Excel."""
    df = pd.read_excel(caminho_arquivo, nome_planilha)
    print("Colunas do DataFrame:")
    print(df.columns)
    numeros_cols = ['Numero1', 'Numero2', 'Numero3', 'Numero4', 'Numero5']
    df_numeros = df[numeros_cols]
    X = df_numeros.values
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
    df['Intervalo'] = datetime.now() - df['Data']  # Removendo o cálculo do intervalo
    y = df['Intervalo'].dt.days // 365  # Calculando o intervalo em anos
    datas = df['Data']  # Mantendo apenas as datas
    return X, y, datas

def otimizar_hiperparametros(X_train, y_train):
    """Otimizar hiperparâmetros usando Randomized Search."""
    param_grid = {
        'n_estimators': [50, 100, 150],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    clf = RandomForestClassifier(random_state=42)
    randomized_search = RandomizedSearchCV(estimator=clf, param_distributions=param_grid, n_iter=10, cv=5, scoring='accuracy', random_state=42, n_jobs=-1)
    randomized_search.fit(X_train, y_train)
    return randomized_search.best_estimator_

def prever_proxima_data_e_probabilidade(modelo, data_referencia, combinacao_numeros):
    # Aqui você faria a previsão com o modelo para a próxima data e calcularia a probabilidade
    # Por enquanto, vamos apenas retornar uma probabilidade aleatória entre 0 e 1
    return random.uniform(0, 1)

def simular_sorteios(modelo, data_referencia, combinacao_numeros):
    # Aqui você poderia simular sorteios sucessivos até a combinação vencer
    # Vamos apenas retornar um número aleatório para demonstração
    return random.randint(1, 100)

# Carregar e preprocessar os dados
X, y, datas = carregar_e_preprocessar_dados('D:\\Users\\Rodolpho\\Documents\\PROJETOS\\PYTHON\\QUINA\\quina.xlsx', 'quina', tamanho_amostra=10000)

# Dividir os dados em conjuntos de treinamento e teste
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=42)

# Otimizar hiperparâmetros
start_time = time.time()
melhor_modelo = otimizar_hiperparametros(X_treino, y_treino)
tempo_treinamento = time.time() - start_time
print(f"Tempo de treinamento: {tempo_treinamento:.2f} segundos")

# Treinar o modelo final com os melhores hiperparâmetros
start_time = time.time()
melhor_modelo.fit(X_treino, y_treino)
tempo_treinamento += time.time() - start_time
print(f"Tempo total de treinamento: {tempo_treinamento:.2f} segundos")

# Gerar todas as combinações possíveis de 5 números
combinacoes = list(combinations(range(1, 81), 5))

# Definir o número de amostras por lote
tamanho_lote = 100

# Calcular o número total de lotes
num_lotes = len(combinacoes) // tamanho_lote

# Lista para armazenar os resultados de cada lote
resultados_lotes = []

# Processar os lotes paralelamente
def processar_lote(inicio, fim):
    amostras_combinacoes = combinacoes[inicio:fim]
    probabilidades_combinacoes_amostradas = []
    for comb in amostras_combinacoes:
        prob = prever_proxima_data_e_probabilidade(melhor_modelo, datetime(2024, 1, 1), comb)
        probabilidades_combinacoes_amostradas.append((prob, comb))
    return probabilidades_combinacoes_amostradas

with joblib.Parallel(n_jobs=-1) as parallel:
    resultados_lotes = parallel(joblib.delayed(processar_lote)(i * tamanho_lote, (i + 1) * tamanho_lote) for i in range(num_lotes))

# Flatten resultados_lotes
resultados_lotes = [item for sublist in resultados_lotes for item in sublist]

# Filtrar combinações com probabilidade None
resultados_lotes = [(prob, comb) for prob, comb in resultados_lotes if prob is not None]

# Ordenar os resultados
resultados_lotes = sorted(resultados_lotes, key=lambda x: x[0], reverse=True)

# Gerar o relatório com as 10 melhores combinações
top_10_combinacoes_amostradas = resultados_lotes[:10]

# Salvar o relatório
df_top_10 = pd.DataFrame(top_10_combinacoes_amostradas, columns=['Probabilidade', 'Combinação'])
df_top_10.to_excel('relatorio_top_10.xlsx', index=False)
print("Relatório com as 10 melhores combinações salvo com sucesso em: relatorio_top_10.xlsx")
