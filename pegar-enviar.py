from banco_de_dados import IaraDB
from whatsapp import EnviarFoto
from whatsapp import EnviarMsm
from ia import Gpt, Processamento
eMsm=EnviarMsm()
eFoto=EnviarFoto()
iaraDb=IaraDB()
processamento=Processamento()
gpt=Gpt()
entrou = False
while True:

    contagem_de_mensagens=iaraDb.contar_tabelas_mensagens_respostas(iaraDb.criar_conexao())
    contagem_de_respostas = contagem_de_mensagens[1]
    contagem_de_mensagens=contagem_de_mensagens[0]
    if contagem_de_mensagens!= contagem_de_respostas:
        resposta_pendente=iaraDb.repostas_pendente(iaraDb.criar_conexao())
        id_msm=resposta_pendente[0]
        numero=resposta_pendente[1]
        msm=resposta_pendente[3]
        #enviarReposta
        if not entrou:
            eMsm.conexao()
            entrou = True
        else:
            pass
        #processarResposta
        indetificando=gpt.identificacao(msm)
        if indetificando!='erro':
            print(msm)
            if msm=='user_is_not_here':
                #cadastro_aluno
                link='https://docs.google.com/forms/d/1pujCHzK60qWerhLrI2yDGapQN4L6rnBxrREQFiGSEVc/edit?usp=forms_home&ths=true'
                eMsm.enviarMensagem(numero, f'Olá, tudo bem? eu sou a Iara a inteligência artificial do Pedro II - Campus caxias. Vamos fazer seu cadastro demora menos de 1 minuto. {link} ')


            if '1' == indetificando[0]:


                #SETOR DA ESCOLA
                if indetificando[1] =='1':
                    resposta_enviar=processamento.get_email_setor(iaraDb.criar_conexao(), msm)
                    eMsm.enviarMensagem(numero, resposta_enviar)
                    iaraDb.adicionarResposta(iaraDb.criar_conexao(), id_msm, numero, resposta_enviar )
                elif indetificando[1] =='2':
                    resposta_enviar = processamento.get_email_professor(msm)
                    eMsm.enviarMensagem(numero, resposta_enviar)
                    iaraDb.adicionarResposta(iaraDb.criar_conexao(), id_msm, numero, resposta_enviar)
                elif indetificando[1]=='3':
                    resposta_enviar = processamento.get_email_turma(iaraDb.criar_conexao(), msm)
                    eMsm.enviarMensagem(numero, resposta_enviar)
                    iaraDb.adicionarResposta(iaraDb.criar_conexao(), id_msm, numero, resposta_enviar)

            elif indetificando[0] == '2':
                print(2)
                if indetificando[1] == '1':
                    print(numero)
                    eFoto.send_menu(numero)
                    iaraDb.adicionarResposta(iaraDb.criar_conexao(), id_msm, numero, 'Cardápio enviado.')
                elif indetificando[1] == '2':
                    turma = iaraDb.encontrar_turma_por_numero(numero)
                    eFoto.enviar_horario(turma, numero)
                    iaraDb.adicionarResposta(iaraDb.criar_conexao(), id_msm, numero, 'Horário da turma enviado.')
            else:
                resposta_enviar = gpt.criar_modelo(
                    'Reescreva essa frase: Essa Funcionalidade ainda não foi criada')
                eMsm.enviarMensagem(numero, resposta_enviar)
                iaraDb.adicionarResposta(iaraDb.criar_conexao(), id_msm, numero, resposta_enviar)


        else:
            resposta_enviar = gpt.criar_modelo('Reescreva essa frase: Não consiguimos identificar o que você está dizendo reescreva por favor.')
            eMsm.enviarMensagem(numero, resposta_enviar)
            iaraDb.adicionarResposta(iaraDb.criar_conexao(), id_msm, numero, resposta_enviar)









