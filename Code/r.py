#from scipy.stats import mannwhitneyu
from scipy.stats import ttest_ind
import csv
import copy
from numpy import mean
path_saida = '../output/'
ALPHA = 0.05


def read_csv():
    mycsv = open('../data/new_results.csv', 'r')
    reader = csv.DictReader(mycsv)
    dict_list = []
    for line in reader:
        dict_list.append(line)
    return dict_list


def save_csv(dict_list):
    with open(f'{path_saida}ranking.csv', 'w') as f:
        w = csv.DictWriter(f, dict_list.keys())
        w.writeheader()
        w.writerow(dict_list)


def criar_resumo(respostas):
    resumo = {'build': [], 'mismanaging': [], 'rework': [], 'unnecessarily': [], 'extraneous': [],
              'psychological': [], 'waiting': [], 'knowledge': [], 'ineffective': [], 'opiniao': [],
              'estado': []}
    for resp in respostas:  # percorrendo as respostas de todas as pessoas
        for pergunta in resumo.keys():  # todas as perguntas que fizemos
            resposta = resp[pergunta]
            try:
                resposta = int(resposta)
            except ValueError as _:
                pass
            resumo[pergunta].append(resposta)

    return resumo


def algoritmo(resumo_):
    resumo = copy.deepcopy(resumo_)
    del resumo['estado']
    del resumo['opiniao']
    ranking = {}
    for r in resumo.keys():
        cont = 0  # contador das 'vitorias'
        for r2 in resumo.keys():
            if r == r2:  # nao comparar com ele mesmo
                continue
            stat, p = ttest_ind(resumo[r], resumo[r2], nan_policy="raise")
            if p > ALPHA:
                print(f'{r} < {r2}')
            else:
                cont += 1
                print(f'{r} > {r2}')
        ranking[r] = cont
    return ranking


def criar_ranking(resumo):
    r = algoritmo(resumo)

    print(r)
    r_ = {key: rank for rank, key in enumerate(
        sorted(set(r.values()), reverse=True), 1)}
    rank = {k: r_[v] for k, v in r.items()}
    print(rank)
    for r1 in rank:
        print(f'{rank[r1]}-{r1} ({r[r1]})')
    save_csv(rank)


def create_csv_summary(resumo_):
    resumo = copy.deepcopy(resumo_)
    del resumo['estado']
    del resumo['opiniao']

    with open(f'{path_saida}resumo_respostas.csv', 'w') as f:
        f.write(
            'pergunta, Nunca observei, Observo raramente, Observo ocasionalmente, frequência\n')
        for r in resumo.keys():
            f.write('%s, %d, %d, %d, %d\n' % (r, resumo[r].count(
                0), resumo[r].count(1), resumo[r].count(2), resumo[r].count(3)))


def criar_csv_estados(resumo):
    count_pe = resumo['estado'].count('Pernambuco')
    count_al = resumo['estado'].count('Alagoas')
    count_pb = resumo['estado'].count('Paraíba')
    count_outros = len(resumo['estado']) - count_pe - count_al - count_pb

    with open(f'{path_saida}resumo_estados.csv', 'w') as f:
        f.write('estado, quantidade\n')
        f.write(f'Pernambuco, {count_pe}\n')
        f.write(f'Alagoas, {count_al}\n')
        f.write(f'Paraíba, {count_pb}\n')
        f.write(f'Outros, {count_outros}')


def criar_opinioes(resumo):
    with open(f'{path_saida}opnioes.csv', 'w') as f:
        f.write('opiniao\n')
        for o in resumo['opiniao']:
            if o != "":
                f.write(f'{o}\n')


def main():
    respostas = read_csv()
    #respostas = respostas[: 2]
    resumo = criar_resumo(respostas)
    criar_csv_estados(resumo)

    # create_csv_summary(resumo)
    criar_ranking(resumo)
    criar_opinioes(resumo)


if __name__ == '__main__':
    main()
