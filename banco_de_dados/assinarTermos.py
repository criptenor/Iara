from __future__ import print_function
import os.path
import re
import time
import pymysql
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configurações do banco de dados
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'iara'

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '19VdSLPd5gN9lvV-TCXh7fo0H66kFKQCW0Yiays8NsBA'
SAMPLE_RANGE_NAME = 'cadastro'


def conectar_bd():
    # Conectar ao banco de dados
    conexao = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    return conexao


def ler_dados_planilha():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('../credentials-1.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        return values

    except HttpError as err:
        print(err)


def aluno_existe(numero):
    # Conectar ao banco de dados
    conexao = conectar_bd()

    try:
        # Criar um cursor para executar as consultas
        cursor = conexao.cursor()

        # Verificar se o aluno já existe no banco de dados
        sql_verificar = "SELECT COUNT(*) FROM aluno WHERE numero = %s"
        cursor.execute(sql_verificar, (numero,))
        resultado = cursor.fetchone()

        if resultado[0] == 0:
            return False
        else:
            return True

    except pymysql.Error as erro:
        print(f"Erro ao verificar a existência do aluno: {erro}")

    finally:
        # Fechar o cursor e a conexão com o banco de dados
        cursor.close()
        conexao.close()

def formatar_numero_telefone(numero):
    numero = re.sub(r'[-+\s]', '', numero)  # Remove hífen, sinal de mais e espaços
    if not numero.startswith('55'):
        numero = '55' + numero
    return numero

def inserir_aluno(nome, turma, numero, assinatura1, assinatura2):
    # Conectar ao banco de dados
    conexao = conectar_bd()

    try:
        # Criar um cursor para executar as consultas
        cursor = conexao.cursor()

        # Verificar se o aluno já existe no banco de dados
        if aluno_existe(numero):
            print(f"Aluno {nome} já existe no banco de dados. Ignorando inserção.")
            return
        else:
            # Inserir o aluno no banco de dados
            sql_inserir = "INSERT INTO aluno (nome, turma, numero, assinatura1, assinatura2) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_inserir, (nome, turma, numero, assinatura1, assinatura2))
            conexao.commit()

            # Imprimir mensagem de sucesso
            print(f"Aluno {nome} inserido com sucesso!")

    except pymysql.Error as erro:
        # Em caso de erro, desfazer a transação
        conexao.rollback()
        print(f"Erro ao inserir aluno: {erro}")

    finally:
        # Fechar o cursor e a conexão com o banco de dados
        cursor.close()
        conexao.close()


def inserir_alunos_planilha():
    # Ler os dados da planilha do Google
    dados_planilha = ler_dados_planilha()

    if not dados_planilha:
        print('No data found.')
        return

    for row in dados_planilha:
        nome = row[1]
        turma = row[2]
        numero = formatar_numero_telefone(row[3])
        assinatura1 = row[4]
        assinatura2 = row[4]

        if assinatura1.strip() == 'Sim! Estou ansioso para utilizar a Iara.':
            assinatura1 = True
        else:
            assinatura1 = False

        if assinatura2.strip() == 'Sim! Estou ansioso para utilizar a Iara.':
            assinatura2 = True
        else:
            assinatura2 = False

        # Inserir o aluno no banco de dados, se não existir
        inserir_aluno(nome, turma, numero, assinatura1, assinatura2)


def main():
    while True:
        try:
            inserir_alunos_planilha()
            time.sleep(50)
        except KeyboardInterrupt:
            print('\nProgram terminated by user.')
            break


if __name__ == '__main__':
    main()
