import numpy as np
import pandas as pd
from pathlib import Path
from generate_MPLRegressor import generate_MPL

"""
    Script para geração de séries de carga a partir de um histórico de dados a carga refere-se a carga total de um alimentador
    de de dist. Fonte dos dados: Light S.A (Artigo JCAE 2020 PLANCAP)
    Link análise estatística -> https://www.mathworks.com/help/econ/infer-residuals.html
"""
def load_generator(arq):
        
    # Caminho da base de dados'
    path = Path(__file__).parent / 'BASE_DE_DADOS' / arq
    load_Table = pd.read_csv(path, delimiter = '\t', header = None)
    # convertendo as séries em objeto numpy
    load_tsdata_2 = load_Table.to_numpy()
    # fatiando a série em intervalo de 4 em 4 (cada dado equivale a 15 minutos)
    hourly_tsdata_2 = load_tsdata_2[::4]

    # Importando a função generate_MPLRegressor onde, uma lista deverá ser fornecida em seu argumento, e está retornará o modelo(net_n), o lag(p_n), as saídas esperadas(Y_n), e a saída obtidas pelo modelo de previsão MLPRegressor(Yhat_n)
    p, Mdl, Y, Yhat = generate_MPL(hourly_tsdata_2)

    # definindo um intervalo de horas
    Npoints = 168
    T = len(hourly_tsdata_2)
    pred_hourly_tsdata_2 = np.zeros(Npoints)
    pred_hourly_tsdata_2[:p] = hourly_tsdata_2[:p].flatten()

    if Npoints < Yhat.shape[0]:
        pred_hourly_tsdata_2[p: T] = Yhat[p: Npoints]
    else:
        pred_hourly_tsdata_2[p: T] = Yhat

    t = T
    while t < Npoints:
        aux = np.array(pred_hourly_tsdata_2[t - p: t])
        aux = aux.reshape(-1, p)
        pred_hourly_tsdata_2[t] = Mdl.predict(aux)[0]
        t += 1

    while True:
        n = input('Insira a quantidade de séries desejada ou tecle enter para 11: ')
        if n == '':
            n = 11
            break
        try:
            n = int(n)
            if n > 0:
                n = n
                break
            else:
                print("Insira um valor numérico válido!")
        except ValueError:
            print('Insira um valor numérico válido!')

    pred_hourly_tsdata_2 = pred_hourly_tsdata_2.flatten()
    load_hourly_tsdata_2 = np.zeros((n, Npoints))
    load_hourly_tsdata_2[0,:] = pred_hourly_tsdata_2

    for i in range(n):
        delta_2 = 0.05 * pred_hourly_tsdata_2 * np.random.randn(Npoints)
        load_hourly_tsdata_2[i, :] = pred_hourly_tsdata_2 + delta_2

    load_hourly_tsdata_2 = np.sqrt(3) * 13.8e3 * load_hourly_tsdata_2

    return load_hourly_tsdata_2

if __name__ == '__main__':

    while True:
        Ndl = input('Insira a quantidade de cargas desejada ou tecle enter para 3 cargas: ')
        if Ndl == '':
            Ndl = 3
            break
        try:
            Ndl = int(Ndl)
            if Ndl > 0:
                Ndl = int(Ndl)
                break
            else:
                print('Insira um valor numérico válido e positivo')
        except ValueError as v:
            print('Insira um valor numérico válido')

    save_path = Path(__file__).parent.parent / 'SERIES_GERADAS' / 'load_hourly_series.xlsx'

    with pd.ExcelWriter(save_path) as writer:
        for i in range(Ndl):
            arq = input('Insira o nome do arquivo: ')
            load_hourly_tsdata = load_generator(arq)
            load_hourly_tsdata_df = pd.DataFrame(load_hourly_tsdata)
            load_hourly_tsdata_df.to_excel(writer, sheet_name = f'Carga {i + 1}', index = False, header = None)

    print('Fim')
