from banco_de_dados import IaraDB
from whatsapp import ExtrairMsm
iaraDB=IaraDB()
eMsm=ExtrairMsm()
entrou=False
while True:
    if not entrou:
        eMsm.conexao()
        entrou=True
    else:
        pass
    msm_completa=eMsm.receberMensagem()
    if not msm_completa:
        pass
    else:
        numero=eMsm.formatar_numero_telefone(msm_completa[0])
        print(numero)
        if iaraDB.verificar_aluno(numero):

            iaraDB.inserir_mensagem(iaraDB.criar_conexao(), numero, msm_completa[1])
        else:
            iaraDB.inserir_mensagem(iaraDB.criar_conexao(), numero, 'user_is_not_here')


