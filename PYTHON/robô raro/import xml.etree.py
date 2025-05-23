import tkinter as tk
from tkinter import filedialog
import pymysql
import configparser

# Ler as informações do banco de dados do arquivo INI
config = configparser.ConfigParser()
config.read('config.ini')

host = config.get('database', 'host')
user = config.get('database', 'user')
password = config.get('database', 'password')
db_name = config.get('database', 'db_name')

# Criar a janela de diálogo para selecionar a pasta XML
root = tk.Tk()
root.withdraw()
pasta_xml = filedialog.askdirectory()
root.destroy()

# Carregar o arquivo XML
arquivo_xml = f"{pasta_xml}/notafiscal.xml"

# Conectar ao banco de dados
connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    db=db_name,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with connection.cursor() as cursor:
        # Percorrer as notas fiscais no arquivo XML
        tree = ET.parse(arquivo_xml)
        root = tree.getroot()
        for notafiscal in root.findall('notafiscal'):
            cnpjcpf = notafiscal.find('cnpjcpf').text
            idpessoa = notafiscal.find('idpessoa').text

            # Verificar se o CNPJ da pessoa está habilitado para cópia
            cursor.execute("SELECT id FROM pessoa WHERE cnpjcpf = %s AND libera_copia = %s", (cnpjcpf, 1))
            result = cursor.fetchone()

            if result:
                # Inserir a nota fiscal no banco de dados
                numero = notafiscal.find('numero').text
                serie = notafiscal.find('serie').text
                dataemissao = notafiscal.find('dataemissao').text
                total = notafiscal.find('total').text
                nota = notafiscal.tostring(method='text', encoding='utf-8').decode('utf-8')

                sql = """
                    INSERT INTO notafiscal (numero, serie, cnpjcpf, idpessoa, dataemissao, total, nota)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (numero, serie, cnpjcpf, idpessoa, dataemissao, total, nota))

    # Confirmar as alterações no banco de dados
    connection.commit()
finally:
    connection.close()