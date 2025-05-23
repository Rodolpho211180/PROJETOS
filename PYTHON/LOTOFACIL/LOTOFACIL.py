import pandas as pd
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from itertools import combinations
import time
from tkinter import filedialog
import tkinter as tk

def load_and_preprocess_data(file_path: str, sheet_name: str, sample_size: int = None) -> tuple:
    """Load and preprocess the data from an Excel file."""
    df = pd.read_excel(file_path, sheet_name, usecols="B:P")  # Selecionando colunas relevantes
    if sample_size and sample_size < len(df):
        df = df.sample(n=sample_size, random_state=42)
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
    df['Intervalo'] = (datetime.now() - df['Data']).dt.days // 365
    X = df.iloc[:, 1:16].values  # Selecionar apenas os primeiros 15 números
    y = df['Intervalo'].values
    return X, y

def optimize_hyperparameters(X_train, y_train):
    """Optimize hyperparameters using Grid Search."""
    param_grid = {
        'n_estimators': [50, 100, 150],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    clf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=clf, param_grid=param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_

def predict_next_draw_date_and_probability(model, data, combination):
    """Predict the next draw date and probability for a given combination."""
    intervalo_pred = model.predict([combination])[0]
    if abs(intervalo_pred - (data - datetime(2024, 1, 1)).days // 365) <= 1:
        prob = model.predict_proba([combination])[0][1]
        return prob if prob is not None else 0
    else:
        return 0

def simulate_draws(model, data, combination):
    """Simulate draws until the combination is correct."""
    acertos = 0
    while True:
        intervalo_pred = model.predict([combination])[0]
        if abs(intervalo_pred - (data - datetime(2024, 1, 1)).days // 365) <= 1:
            acertos += 1
            break
        acertos += 1
    return acertos

# Carregar e preprocessar os dados
X, y = load_and_preprocess_data('D:\\Users\\Rodolpho\\Documents\\PROJETOS\\PYTHON\\LOTOFACIL\\lotofacil.xlsx', 'lotofacil', sample_size=10000)

# Dividir os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Otimizar hiperparâmetros
start_time = time.time()
best_model = optimize_hyperparameters(X_train, y_train)
training_time = time.time() - start_time
print(f"Tempo de treinamento: {training_time:.2f} segundos")

# Treinar o modelo final com os melhores hiperparâmetros
start_time = time.time()
best_model.fit(X_train, y_train)
training_time += time.time() - start_time
print(f"Tempo total de treinamento: {training_time:.2f} segundos")

# Gera todas as combinações possíveis de 15 números
combinacoes = list(combinations(range(1, 26), 15))

# Calcular as probabilidades de sucesso para todas as combinações e classificar
probabilidades_combinacoes = []
total_combinacoes = len(combinacoes)
start_time = time.time()
for i, comb in enumerate(combinacoes):
    prob = predict_next_draw_date_and_probability(best_model, datetime(2024, 1, 1), comb)
    probabilidades_combinacoes.append((prob, comb))
    # Imprimir progresso a cada 10% completado
    if (i + 1) % (total_combinacoes // 10) == 0:
        progresso = ((i + 1) / total_combinacoes) * 100
        elapsed_time = time.time() - start_time
        estimated_time = (elapsed_time / (i + 1)) * (total_combinacoes - (i + 1))
        print(f"Progresso: {progresso:.1f}% concluído. Tempo decorrido: {elapsed_time:.2f} segundos. Estimativa de tempo restante: {estimated_time:.2f} segundos")

# Filtrar combinações com probabilidade None
probabilidades_combinacoes = [(prob, comb) for prob, comb in probabilidades_combinacoes if prob is not None]

# Ordenar as probabilidades
probabilidades_combinacoes = sorted(probabilidades_combinacoes, key=lambda x: x[0], reverse=True)

# Gerar o relatório com as 10 melhores combinações
top_10_combinacoes = probabilidades_combinacoes[:10]

# Obter o diretório para salvar o arquivo
root = tk.Tk()
root.withdraw()
file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos do Excel", "*.xlsx")], title="Salvar Relatório")
root.destroy()

if file_path:
    df_top_10 = pd.DataFrame(top_10_combinacoes, columns=['Probabilidade', 'Combinação'])
    df_top_10.to_excel(file_path, index=False)
    print("Relatório com as 10 melhores combinações salvo com sucesso em:", file_path)
else:
    print("Nenhum diretório selecionado. Relatório não foi salvo.")

# Imprimir as 10 melhores combinações e o número de jogos necessários
for i, (prob, combination) in enumerate(top_10_combinacoes):
    num_jogos = simulate_draws(best_model, datetime(2024, 1, 1), combination)
    print(f"{i+1}. {combination} com {prob:.2f}% de chance de acerto. Número de jogos necessários: {num_jogos}")
