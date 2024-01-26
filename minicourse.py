from time import sleep
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-3.5-turbo"

def informar_aluno(aluno, disciplina, frequencia, situacao, nota1, nota2, media):
    return f'Aluno: ${aluno}, Disciplina: ${disciplina}, Frequência: ${frequencia}, Situação: ${situacao}, Nota 1: ${nota1}, Nota 2: ${nota2}, Média: ${media}'

LISTA_DISCIPLINAS = ('Programação III', 'Engenharia de Software', 'Construção de Sites II', 'Tópicos Especiais I')

todos_alunos = []

print('Sistema iniciando...')
sleep(3)
print('INICIADO')

while True:

    sistema = {}

    opcao = str(input('Olá, deseja registrar alguma aluno: S/N ')).strip()

    if opcao.upper() == 'S':
        aluno = str(input('Qual é o nome do aluno? ')).strip()

        sistema['aluno'] = aluno

        while True:
            disciplina = int(input('''Qual a disciplina?
0 - Programação III
1 - Engenharia de Software
2 - Construção de Sites II
3 - Tópicos Especiais I
'''))
            
            if disciplina in range(4):
                break
            
        for index, nome_disciplina in enumerate(LISTA_DISCIPLINAS):
            if index == disciplina:
                sistema['disciplina'] = nome_disciplina
        
        nota1 = float(input('Qual foi a primeira nota? '))

        nota2 = float(input('Qual foi a segunda nota? '))

        media = (nota1 + nota2) / 2

        frequencia = float(input('Qual a frequência? '))

        sistema['frequencia'] = frequencia

        situacao = 'APROVADO' if media >= 6 and frequencia >= 75.0 else 'REPROVADO'

        sistema['situacao'] = situacao

        todos_alunos.append(sistema)

        while True:
            escolha = str(input('Quer ver os alunos registrados? S/N ')).strip()

            if escolha.upper() == 'S':
                print(todos_alunos)
                break

            elif escolha.upper() == 'N':
                print('IA gerando algo...')
                
                prompt_system = '''
                    Você é um funcionário da instituição deste aluno e deve avaliar seu desempenho.
                    # formato de saída:
                        um resumo sobre o desempenho do aluno.
                        obs: caso tenha dados estranho como mais de 100 de frequência ou menos que 0, e notas acima de 10 ou abaixo de 0.
                        informe que pode ter ocorrido um erro de digitação e tente estipular o valor que deveria te sido digitado.
                '''
                prompt_user = informar_aluno(sistema['aluno'],sistema['disciplina'],sistema['frequencia'],sistema['situacao'], nota1, nota2, media)

                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": prompt_system
                        },
                        {
                            "role": "user",
                            "content": prompt_user
                        }
                    ]
                )
                print(response.choices[0].message.content)
                break

            else:
                print('Valor inválido! Responda S - SIM ou N -NÃO')

    elif opcao.upper() == 'N':
        break

    else:
        print('Valor inválido! Escolha entre S - SIM ou N - NÃO')

print('Sistema desligando...')
sleep(3)
print('DESLIGADO')
