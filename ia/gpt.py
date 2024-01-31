import openai
from banco_de_dados import IaraDB
iaraDB=IaraDB()
openai.api_key = "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"
class Gpt():
    def criar_modelo(self, prompt):

        model_engine = "text-davinci-003"
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        response = completion.choices[0].text
        return response

    def identificacao(self, inde):
        inde = inde.lower()

        # Indentificando _______ 1 ________ EMAIL __________
        if 'email' in inde or 'e-mail' in inde:
            print("i1")
            nome_professor = self.criar_modelo(
                f"retire somente o nome da frase a seguir e retorne o nome: frase[{inde}]")
            nome_professor = nome_professor.replace("Professora", "")
            nome_professor = nome_professor.replace("professora", "")
            nome_professor = nome_professor.replace("professor", "")
            nome_professor = nome_professor.replace("Professor", "")

            print(nome_professor)
            if iaraDB.encontrar_email_por_parte_nome_professor(iaraDB.criar_conexao(), nome_professor.strip()) != None:
                print(1.2)
                return '1', '2'


            elif 'soep' in inde or 'direção geral' in inde or 'Nutrição' in inde or 'direção pedagógica' in inde or 'napne' in inde or 'reito' in inde or 'iara' in inde:
                print(1.1)
                return '1', '1'

            for turma in iaraDB.obter_ids_turma(iaraDB.criar_conexao()):
                if turma.lower() in inde.lower() :
                    print(1.3)
                    return '1', '3'
            return 'erro'



        # Indentificando _______ 2 ________ Horários __________
        elif 'cardápio' in inde \
                or 'cardapio' in inde \
                or 'horario' in inde \
                or 'hora' in inde \
                or 'horário' in inde \
                or 'horário da aula' in inde \
                or 'lab' in inde \
                or 'horário' in inde \
                or 'aula' in inde:

            if 'cardápio' in inde or 'cardapio' in inde or 'cardápio de hoje' in inde or 'cardapio da semana' in inde or 'almoço' in inde or 'lanche' in inde:
                print(2.1)
                return '2', '1'
            elif 'horário da minha aula' in inde or 'horario da minha aula' in inde or 'horario da aula ' in inde or 'hora' in inde and 'aula' in inde or 'aula' in inde:
                print(2.2)
                return '2', '2'
            print("i2")


        # Indentificando _______ 3 ________ Calendários __________
        elif 'pfv' in inde or 'prova final' in inde or 'calendário' in inde or 'calendario' in inde:
            if 'pfv' in inde or 'prova final' in inde:
                print(3.1)
                return '3', '1'
            elif 'calendario anual' in inde or 'calendário de 2023' in inde or 'qual calendario' in inde:
                print(3.2)
                return '3', '2'
            print("i3")


        # Indentificando _______ 4 ________ Saudação __________
        elif 'oi' == inde or 'olá' == inde or 'iara' == inde or 'ola' == inde:
            print("i4")
            print(4.1)
            return '4', '1'

        elif 'baixar' in inde or 'download' in inde or 'boletim' in inde:
            print("i6")
            if 'musica' in inde or 'música' in inde or 'mp3' in inde:
                print(6.1)
                return '6', '1'
            elif 'video' in inde or 'vídeo' in inde or 'videos' in inde:
                print(6.2)
                return '6', '2'
            elif 'notas' in inde or 'boletim' in inde or 'nota' in inde:
                print(6.3)
                return '6', '3'
            elif 'foto' in inde or 'imagem' in inde:
                print(6.4)
                return '6', '4'
            else:
                return "erro1"
        elif 'regimento interno do cp2' in inde \
                or 'regimento interno' in inde \
                or 'estatuto do grêmio' in inde \
                or 'código de ética' in inde \
                or 'codigo de etica' in inde \
                or 'codigo de ética' in inde \
                or 'código de etica' in inde \
                or ' estatuto' in inde:
            print("i7")

            if 'regimento interno do cp2' in inde or 'regimento interno' in inde or 'regimento' in inde:
                print(7.2)
                return '7', '1'
            elif 'código de ética' in inde or 'codigo de etica' in inde or 'codigo de ética' in inde or 'código de etica' in inde or 'regimento' in inde:
                print(7.1)
                return '7', '2'
            elif 'estatuto do gremio' in inde or 'estatuto do grêmio' in inde or 'estatuto' in inde:
                print(7.3)
                return '7', '3'


        # Indentificando _______ 5 ________ GENERIC __________
        else:
            print("i5")
            if 'cp2' in inde or 'colégio' in inde or 'escola' in inde or 'reitoria' in inde or 'hino' in inde or 'tabuada' in inde or 'campus' in inde or 'diretor' in inde or 'reito' in inde or 'uniforme' in inde or 'diretor' in inde or 'auxílio' in inde or 'auxilio' in inde:

                print(5.1)
                return '5', '1'

            elif 'criou você' in inde or 'quem criou voce?' == inde or 'quem é você?' == inde:
                print(5.2)
                return '5', '2'
            else:
                print(5.3)
                return '5', '3'

        # Generate a response

