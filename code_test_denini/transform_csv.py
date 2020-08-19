import csv

QUESTIONS = {'Desenvolver uma funcionalidade que não atende o que foi requisitado pelo cliente. (Building the wrong feature or product)': 'build',
             'Distribuição desordenada de tarefas. (Mismanaging the backlog)': 'mismanaging',
             'Trabalhar em tarefas que já foram encerradas e deveriam esta corretas, gerando retrabalho. (Rework)': 'rework',
             'Desenvolvimento de códigos complexos, para solucionar coisas simples. (Unnecessarily complex solutions)': 'unnecessarily',
             'Sobrecarga de trabalho, estar envolvido em várias etapas do processo de desenvolvimento ao mesmo tempo. (Extraneous cognitive load)': 'extraneous',
             'Emocionalmente abalado, excesso de cobranças e conflitos, sejam pessoais ou do ambiente de trabalho. (Psychological distress)': 'psychological',
             'Excesso de tempo ocioso e atribuição de tarefas multidisciplinares. (Waiting/multitasking)': 'waiting',
             'Má gestão do conhecimento. (Knowledge loss)': 'knowledge',
             'Falhas na comunicação, falta de diálogo e falta de entrosamento das pessoas ao se comunicarem.  (Ineffective communication)': 'ineffective',
             }

QUESTIONS_OPINION = {'10 - Adicione uma perda de produtividade que você acha relevante, mas não consta neste formulário.  ': 'opiniao',
                     '11 - Em que estado você trabalha?': 'estado',
                     'Caso você queria receber os resultados dessa pesquisa, informe seu e-mail.': 'email'}


def read_csv():
    mycsv = open('results2.csv', 'r')
    reader = csv.DictReader(mycsv)
    dict_list = []
    for line in reader:
        dict_list.append(line)
    return dict_list


def save_csv(dict_list):
    with open('new_results2.csv', 'w') as f:
        w = csv.DictWriter(f, dict_list[0].keys())
        w.writeheader()
        for d in dict_list:
            w.writerow(d)


if __name__ == '__main__':
    dict_list = read_csv()
    new_dicts = []
    for answer in dict_list:
        new = {}
        for question in QUESTIONS.keys():
            a = answer[question]
            # traducao da resposta para um termo mais facil
            if 'Nunca observei' in a:
                a = '0'
            elif 'Observo raramente' in a:
                a = '3'
            elif 'Observo ocasionalmente' in a:
                a = '2'
            elif 'frequência' in a:
                a = '1'
            else:
                print('--->ERROR: Unknown question: %s' % a)

            new[QUESTIONS[question]] = a  # fazendo a traducao da pergunta tbm

        for question in QUESTIONS_OPINION.keys():  # mesma coisa, mas para as perguntas abertas
            a = answer[question]
            new[QUESTIONS_OPINION[question]] = a

        new_dicts.append(new)

    save_csv(new_dicts)
