import wikipedia
from googleapiclient.discovery import build
import PyPDF2
import time
import tkinter as tk
from tkinter import filedialog
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import sqlite3

# Connect to the database and create the 'conversas' table if it does not exist
conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS conversas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT,
                    resposta TEXT
                  )''')
conn.commit()

# Função para extrair texto de um arquivo PDF
def extrair_texto_pdf(caminho_arquivo):
    texto = ""
    with open(caminho_arquivo, 'rb') as file:
        leitor = PyPDF2.PdfFileReader(file)
        for pagina in range(leitor.numPages):
            texto += leitor.getPage(pagina).extractText()
    return texto

# Função para buscar informações na Wikipedia
def buscar_wikipedia(consulta):
    try:
        return wikipedia.summary(consulta, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        return "A consulta é ambígua. Por favor, seja mais específico."
    except wikipedia.exceptions.PageError as e:
        return "Não foi possível encontrar informações sobre o tópico."

# Função para buscar informações na web usando a API do Google
def buscar_google(consulta, api_key, cse_id):
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=consulta, cx=cse_id).execute()
        if 'items' in res:
            return res['items'][0]['snippet']
        else:
            return "Não foi possível encontrar informações na web."
    except Exception as e:
        print("Erro ao buscar informações na web:", e)
        return "Ocorreu um erro ao buscar informações na web."

# Função para iniciar a conversa com o chatbot
def iniciar_conversa(chatbot):
    nome_usuario = input("Por favor, diga seu nome: ")
    print(f"Olá, {nome_usuario}! Como posso ajudá-lo com Python hoje?")
    return nome_usuario

# Função para interagir com o chatbot
def interagir(chatbot, conexao, api_key, cse_id):
    nome_usuario = iniciar_conversa(chatbot)
    while True:
        try:
            # Get user input
            user_input = input("Você: ")

            # Search Wikipedia or Google based on input prefix
            if user_input.startswith("wikipedia"):
                consulta = user_input[10:]
                resposta = buscar_wikipedia(consulta)
            elif user_input.startswith("google"):
                consulta = user_input[7:]
                resposta = buscar_google(consulta, api_key, cse_id)
            else:
                # Get chatbot response for other input
                resposta = chatbot.get_response(user_input)

            print("Bot: ", resposta)

            # Store conversation history in database
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO conversas(usuario, resposta) VALUES (?, ?)", (nome_usuario, str(resposta)))
            conexao.commit()

            # Get feedback and handle continuation
            feedback = input("Você está satisfeito com a resposta? (sim/não): ")
            if feedback.lower() == "não":
                print("Por favor, nos diga como podemos melhorar.")

            if input("Deseja continuar? (sim/não): ").lower() != "sim":
                break

        except KeyboardInterrupt:
            print("A interação foi interrompida.")
            break

# Aqui você precisará preencher com as informações apropriadas para sua API do Google e banco de dados SQLite
api_key = "AIzaSyAmgEdiDfplZqyS-hstOVhIFyISJZn_vso"
cse_id = "622515576b09346c5"

# Configuração e treinamento do chatbot
chatbot = ChatBot("PyBot")
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.portuguese")

# Chamar a função interagir com todos os argumentos necessários
interagir(chatbot, conn, api_key, cse_id)

# Fechar a conexão com o banco de dados ao final
conn.close()
