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
              'psychological': [], 'waiting': [], 'knowledge': [], 'ineffective': []}
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

    with open(f'{path_saida}resumo_respostas.csv', 'w') as f:
        f.write(
            'pergunta, Nunca observei, Observo raramente, Observo ocasionalmente, frequência\n')
        for r in resumo.keys():
            f.write('%s, %d, %d, %d, %d\n' % (r, resumo[r].count(
                0), resumo[r].count(1), resumo[r].count(2), resumo[r].count(3)))


def main():
    respostas = read_csv()
    resumo = criar_resumo(respostas)
    create_csv_summary(resumo)
    criar_ranking(resumo)


if __name__ == '__main__':
    main()
