from ia import Gpt
from banco_de_dados import IaraDB
from whatsapp import EnviarFoto
iaraDB=IaraDB()
eFoto=EnviarFoto()
gpt=Gpt()
class Processamento():
    def get_email_professor(self, msm):
        # Nome do professor desejado
        nome_professor = gpt.criar_modelo(
            f"retire somente o nome da frase a seguir e retorne o nome: frase[{msm}]").lower()


        nome_professor = (nome_professor.lower()).strip()
        print(nome_professor, '=====================Nome inicial')
        email=iaraDB.encontrar_email_por_parte_nome_professor(iaraDB.criar_conexao(), nome_professor)
        if email != None:

            return f'{gpt.criar_modelo(f"escreva isso de maneira diferente: O email do professor {nome_professor} que você pediu é: ")} {email}'
        else:

            return f'Não encontramos o Professor, tente reescrever!'

    def get_email_setor(self, conexao, mensagem):
        cursor = conexao.cursor()

        # Consulta SQL para obter os nomes de todos os setores
        sql = "SELECT nome FROM setor"
        cursor.execute(sql)
        nomes_setores = [row[0] for row in cursor.fetchall()]

        # Verifica se algum nome de setor está contido na mensagem
        setores_encontrados = []
        for nome_setor in nomes_setores:
            if nome_setor.lower() in mensagem.lower():
                setores_encontrados.append(nome_setor)

        # Verifica se foram encontrados setores na mensagem
        if setores_encontrados:
            emails_setores = []
            for nome_setor in setores_encontrados:
                # Consulta SQL para obter o e-mail do setor pelo nome
                sql = "SELECT email FROM setor WHERE nome = %s" \
                      "Limit 1"
                cursor.execute(sql, (nome_setor,))
                resultado = cursor.fetchone()
                if resultado:
                    email_setor = resultado[0]
                    emails_setores.append(email_setor)

            email=gpt.criar_modelo(f"Escreva isso de outra forma:'email do setor que voce pediu é:")
            email=email+' '+emails_setores[0]
            return email
        else:
            return None

    def get_email_turma(self, conexao, mensagem):
        cursor = conexao.cursor()

        # Consulta SQL para obter todos os id_turma
        sql = "SELECT id_turma FROM turma"
        cursor.execute(sql)
        resultados = cursor.fetchall()

        # Lista para armazenar os id_turma encontrados
        id_turmas = []

        for resultado in resultados:
            id_turma = resultado[0]
            if str(id_turma) in mensagem:
                id_turmas.append(id_turma)

        # Verificar se há id_turma encontrados
        if id_turmas:
            # Consulta SQL para obter o e-mail das turmas encontradas
            sql = "SELECT email FROM turma WHERE id_turma IN ({})".format(
                ", ".join(str(id_turma) for id_turma in id_turmas))
            cursor.execute(sql)
            emails = cursor.fetchall()

            # Lista para armazenar os e-mails das turmas encontradas
            email_turmas = [email[0] for email in emails]

            return email_turmas
        else:
            return None








