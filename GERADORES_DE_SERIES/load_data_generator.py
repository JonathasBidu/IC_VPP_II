import numpy as np
import pandas as pd
from generate_MPLRegressor import generate_MPL

"""
    Script para geração de séries de carga a partir de um histórico de dados a carga refere-se a carga total de um alimentador
    de de dist. Fonte dos dados: Light S.A (Artigo JCAE 2020 PLANCAP)
    Link análise estatística -> https://www.mathworks.com/help/econ/infer-residuals.html
"""
def load_generator():
        
    # Caminho da base de dados'
    path_1 = 'C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP_II\\BASE_DE_DADOS\\Dafeira_load.TXT'
    path_2 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP_II\\BASE_DE_DADOS\\Bandeira_load.txt"
    load_Table_2 = pd.read_csv(path_2, delimiter = '\t', header = None)
    # convertendo as séries em objeto numpy
    load_tsdata_2 = load_Table_2.to_numpy()
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


