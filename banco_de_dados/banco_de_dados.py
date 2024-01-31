import pymysql
from datetime import datetime
import socket

class IaraDB:
    def criar_conexao(self):
        def is_localhost_in_use():
            try:
                # Tenta criar uma conexão com o endereço "localhost"
                socket.create_connection(("localhost",
                                          3306))  # Substitua a porta 3306 pela porta correta do seu servidor MySQL, se necessário
                return False  # O endereço "localhost" está disponível
            except ConnectionRefusedError:
                return True  # O endereço "localhost" está em uso
            except OSError:
                return True

        while True:
            if not is_localhost_in_use():
                # Configurações de conexão
                config = {
                    'user': 'root',
                    'password': '',
                    'host': 'localhost',
                    'database': 'iara',
                    'autocommit': True
                }
                # Cria uma conexão com o banco de dados
                conn = pymysql.connect(**config)
                return conn
            else:
                pass

    def encontrar_email_por_nome_professor(self, conn, nome_professor):
        cursor = conn.cursor()

        # Executa a consulta SQL para encontrar o email do professor pelo nome
        cursor.execute("SELECT email FROM professor WHERE nome = %s", (nome_professor,))
        resultado = cursor.fetchone()

        # Verifica se o professor foi encontrado
        if resultado is not None:
            email = resultado[0]
        else:
            email = None

        # Fecha o cursor e a conexão
        cursor.close()
        return email

    def inserir_mensagem(self, conn, numero, mensagem):
        # Obtém o horário atual (apenas hora e minuto)
        horario = datetime.now().strftime('%H:%M')

        # Cria um cursor para executar comandos SQL
        cursor = conn.cursor()

        # Comando SQL para verificar se o número já registrou a mesma mensagem no mesmo minuto
        sql_check = 'SELECT COUNT(*) FROM mensagens_recebidas WHERE numero = %s AND mensagem = %s AND horario LIKE %s'
        values_check = (numero, mensagem, horario + '%')

        # Executa o comando SQL para verificar se a mensagem já foi registrada no mesmo minuto
        cursor.execute(sql_check, values_check)
        result = cursor.fetchone()

        if result[0] == 0:
            # Comando SQL para inserir a mensagem na tabela
            sql_insert = 'INSERT INTO mensagens_recebidas (numero, mensagem, horario) VALUES (%s, %s, %s)'
            values_insert = (numero, mensagem, horario)

            # Executa o comando SQL para inserir a mensagem
            cursor.execute(sql_insert, values_insert)

        # Fecha o cursor
        cursor.close()

    def contar_tabelas_mensagens_respostas(self, conn):
        # Cria um cursor para executar comandos SQL
        cursor = conn.cursor()

        # Consulta o número de registros de respostas
        sql_respostas = 'SELECT COUNT(*) FROM resposta'
        cursor.execute(sql_respostas)
        numero_respostas = cursor.fetchone()[0]

        # Consulta o número de registros de perguntas
        sql_perguntas = 'SELECT COUNT(*) FROM mensagens_recebidas'
        cursor.execute(sql_perguntas)
        numero_perguntas = cursor.fetchone()[0]

        # Fecha o cursor
        cursor.close()

        return numero_respostas, numero_perguntas

    def repostas_pendente(self, conn):
        # Cria um cursor para executar comandos SQL
        cursor = conn.cursor()

        # Consulta a mensagem mais antiga sem resposta
        sql = '''
               SELECT mr.id, mr.numero, mr.horario, mr.mensagem
               FROM mensagens_recebidas mr
               LEFT JOIN resposta r ON mr.id = r.id_mensagem
               WHERE r.id_mensagem IS NULL
               ORDER BY mr.horario ASC
               LIMIT 1
           '''

        cursor.execute(sql)
        mensagem_sem_resposta = cursor.fetchone()

        # Fecha o cursor
        cursor.close()

        return mensagem_sem_resposta

    def adicionarResposta(self, conn, id_mensagem, numero, resposta):
        # Cria um cursor para executar comandos SQL
        cursor = conn.cursor()

        # Obtém o horário atual
        horario = datetime.now().strftime('%H:%M')

        # Insere a resposta na tabela "resposta"
        sql_insert = '''
            INSERT INTO resposta (id_mensagem, numero, horario, resposta)
            VALUES (%s, %s, %s, %s)
        '''
        values_insert = (id_mensagem, numero, horario, resposta)

        cursor.execute(sql_insert, values_insert)

        # Fecha o cursor
        cursor.close()

    def obter_ids_turma(self, conn):
        cursor = conn.cursor()

        # Executa a consulta SQL para obter todos os IDs de turma
        cursor.execute("SELECT id_turma FROM turma")
        resultados = cursor.fetchall()

        # Extrai os IDs de turma dos resultados
        ids_turma = [resultado[0] for resultado in resultados]

        # Fecha o cursor
        cursor.close()

        return ids_turma

    def encontrar_email_por_parte_nome_professor(self, conn, parte_nome):
        cursor = conn.cursor()

        # Executa a consulta SQL para encontrar o email do professor por parte do nome
        cursor.execute("SELECT email FROM professor WHERE nome LIKE %s", f"%{parte_nome}%")
        resultado = cursor.fetchone()

        # Verifica se há resultado e retorna o email encontrado
        if resultado:
            email = resultado[0]
        else:
            email = None

        # Fecha o cursor
        cursor.close()

        # Caso não encontre nenhum resultado, retorna None
        return email

    def encontrar_email_por_nome_setor(self, conexao, nome_setor):
        cursor = conexao.cursor()

        # Consulta SQL para encontrar o e-mail do setor pelo nome
        sql = "SELECT email FROM setor WHERE nome = %s"
        cursor.execute(sql, (nome_setor,))
        resultado = cursor.fetchone()

        if resultado:
            email_setor = resultado[0]
        else:
            email_setor = None

        # Fecha o cursor
        cursor.close()

        return email_setor

    def inserir_aluno(self, nome, turma, numero, assinatura1, assinatura2):
        # Conectar ao banco de dados
        conexao = pymysql.connect(host='localhost', user='root', password='', database='iara')

        try:
            # Criar um cursor para executar as consultas
            cursor = conexao.cursor()

            # Montar o comando SQL para inserir o aluno
            sql = "INSERT INTO aluno (nome, turma, numero, assinatura1, assinatura2) VALUES (%s, %s, %s, %s, %s)"
            valores = (nome, turma, numero, assinatura1, assinatura2)

            # Executar a consulta SQL
            cursor.execute(sql, valores)

            # Confirmar a transação
            conexao.commit()

            # Imprimir mensagem de sucesso
            print("Aluno inserido com sucesso!")

        except pymysql.Error as erro:
            # Em caso de erro, desfazer a transação
            conexao.rollback()
            print(f"Erro ao inserir aluno: {erro}")

        finally:
            # Fechar o cursor e a conexão com o banco de dados
            cursor.close()
            conexao.close()

    def verificar_aluno(self, numero):
        try:
            # Criar um cursor para executar as consultas
            cursor = self.criar_conexao().cursor()

            # Montar o comando SQL para verificar se o aluno existe
            sql = "SELECT COUNT(*) FROM aluno WHERE numero = %s"
            valor = (numero,)

            # Executar a consulta SQL
            cursor.execute(sql, valor)

            # Obter o resultado da consulta
            resultado = cursor.fetchone()

            # Verificar se o aluno existe
            if resultado[0] > 0:
                return True
            else:
                return False

        except pymysql.Error as erro:
            pass

        finally:
            # Fechar o cursor
            cursor.close()

    def encontrar_turma_por_numero(self, numero):
        # Conectar ao banco de dados
        conexao = self.criar_conexao()

        try:
            # Criar um cursor para executar as consultas
            cursor = conexao.cursor()

            # Encontrar a turma do aluno com base no número
            sql = "SELECT turma FROM aluno WHERE numero = %s"
            cursor.execute(sql, (numero,))
            resultado = cursor.fetchone()

            if resultado:
                turma = resultado[0]
                print(f"A turma do aluno com número {numero} é: {turma}")
            else:
                print(f"Não foi encontrado um aluno com número {numero}")

        except pymysql.Error as erro:
            print(f"Erro ao encontrar turma por número: {erro}")

        finally:
            # Fechar o cursor e a conexão com o banco de dados
            cursor.close()
            conexao.close()
