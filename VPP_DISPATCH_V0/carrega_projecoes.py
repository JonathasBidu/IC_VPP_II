import pandas as pd
import numpy as np

"""
    Este programa carrega as projeções de carga, geração solar, geração eólica, e dados relacionados da vpp.

    - Parâmetros: (Nt, Nl, Ndl, Npv, Nwt)
        - Nt (int): Número de intervalos de tempo na janela de projeção.
        - Nl (int): Número de séries de carga a serem carregadas.
        - Ndl (int): Número de séries de carga desconectada a serem carregadas.
        - Npv (int): Número de séries de geração solar a serem carregadas.
        - Nwt (int): Número de séries de geração eólica a serem carregadas.

    - Retorna:
        -Tuple: Uma tupla contendo arrays numpy representando as séries temporais de carga, geração solar, 
           geração eólica, carga desconectada de referência, carga desconectada mínima,
           carga desconectada máxima, PLD (Preço de Liquidação de Diferença), e Tau Dist.
           - Atributos:
                - p_l: potência das cargas, shape (Nl, Nt)
                - p_pv: potência das usinas FV, shape (Npv, Nt)
                - p_wt: potência das usinas eólicas, shape (Nwt, Nt)
                - p_dl_ref: potência de referência das cargas (Ndl, Nt)
                - p_dl_min: potência mínima das cargas, shape (Ndl, Nt)
                - p_dl_max: potência máxima das cargas, shape (Ndl, Nt)
                - tau_pdl: tarifa PLD (Preço de Liquidação de Diferença), shape (Nt)
                - tau_dist: tarifa da distribuidora, shape (Nt,)
                - tau_dl: tarifa de abatimento, shape (Nt,)
"""

def projecoes(Nt: int, Nl: int, Ndl: int, Npv: int, Nwt: int)-> tuple[np.ndarray, ...]:

    inicio = 0
    
    # carregamento da série de cargas
    path_1 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP_II\\SERIES_GERADAS\\load_hourly_series.csv"
    load_hourly_series = pd.read_csv(path_1, sep = ';', header = None)
    m, _ = load_hourly_series.shape
    idx = np.random.choice(m, int(Nl))
    p_l = load_hourly_series.iloc[idx, inicio: (inicio + int(Nt))].values/ 1e6

    # carregamento da série de cargas para referência
    path_2 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP_II\\SERIES_GERADAS\\dload_hourly_series.csv"
    dload_hourly_series = pd.read_csv(path_2, sep = ';', header = None)
    m, _ = dload_hourly_series.shape
    idx = np.random.choice(m, int(Ndl))
    p_dl_ref = load_hourly_series.iloc[idx, inicio: (inicio + int(Nt))].values/ 1e6

    # carregamento da série das usinas eólicas
    path_3 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP_II\\SERIES_GERADAS\\WTGsystem_hourly_series.csv"
    WTGpwr_hourly_series = pd.read_csv(path_3, sep = ';', header = None)
    m, _ = WTGpwr_hourly_series.shape
    idx = np.random.choice(m, int(Nwt))
    p_wt = WTGpwr_hourly_series.iloc[idx, inicio: (inicio + int(Nt))].values/ 1e3

    # carregamento da série das usinas fotovoltaicas
    path_4 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP_II\\SERIES_GERADAS\\PVsystem_hourly_series.csv"
    PVpwr_hourly_series = pd.read_csv(path_4, sep = ';', header = None)
    m, _ = PVpwr_hourly_series.shape
    idx = np.random.choice(m, int(Npv))
    p_pv = PVpwr_hourly_series.iloc[idx, inicio: (inicio + int(Nt))].values / 1e3

    # carregamento da série de tarifa do Preço de Liquidação de Diferença (PLD)
    path_5 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP_II\\SERIES_GERADAS\\PLD_hourly_series.csv"
    PLD_hourly_series = pd.read_csv(path_5, header = None, sep = ';')
    tau_pld = PLD_hourly_series.iloc[0, inicio: (inicio + int(Nt))]

    # carregamento da série de tarifa da distribuidora
    path_6 = "C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP_II\\SERIES_GERADAS\\TDist_hourly_series.csv"
    TDist_hourly_series = pd.read_csv(path_6, sep = ';', header = None)
    tau_dist = TDist_hourly_series.iloc[0, inicio: (inicio + int(Nt))]
    tau_dl = 0.15 * TDist_hourly_series.iloc[0, inicio: (inicio + int(Nt))] # Abatimento de 15% sobre o valor da tarifa

    dl_delta_min = np.zeros(int(Ndl))
    dl_delta_max = np.zeros(int(Ndl))

    for i in range(int(Ndl)):
        while True:
            dl_max = input(f'Insira o limite superior da carga {i + 1} ((%) acima da referência) ou tecle enter para 20%: ')
            if dl_max == '':
                dl_max = 20.0 # padrão de 20 por cento de limite de corte de carga superior
                break
            try:
                dl_max = float(dl_max)
                if dl_max > 0:
                    dl_delta_max[i] = dl_max
                    break
                print('Insira um valor real positivo')
            except ValueError:
                print("Informe um valor numérico válido")
    
    for i in range(int(Ndl)):
        while True:
            dl_min = input(f'Insira o limite inferior da carga {i + 1} ((%) abaixo da referência) ou tecle enter para 20%: ')
            if dl_min == '':
                dl_delta_min[i] = 20.0 # Padrão de 20 por cento de limite de corte de carga inferior
                break
            try:
                dl_min = float(dl_min)
                if dl_min > 0:
                    dl_delta_min[i] = dl_min
                    break
                print('Insira um valor real positivo')
            except ValueError:
                print("Informe um valor numérico válido")

    print(' ')
    dl_delta_max = dl_delta_max / 100.0
    dl_delta_min = dl_delta_min / 100.0

    p_dl_max = np.zeros((int(Ndl), int(Nt)))
    p_dl_min = np.zeros((int(Ndl), int(Nt)))

    for i in range(int(Ndl)):
        p_dl_max[i, :] = p_dl_ref[i, :] + dl_delta_max[i] * np.abs(p_dl_ref[i,:])
        p_dl_min[i, :] = p_dl_ref[i, :] - dl_delta_min[i] * np.abs(p_dl_ref[i,:])


    return p_l, p_pv, p_wt, p_dl_ref, p_dl_min, p_dl_max, tau_pld, tau_dist, tau_dl


# # Exemplo de uso
# import matplotlib.pyplot as plt
# from vpp_data import vpp

# data = vpp()

# Nt = 24  # Número de pontos de dados na série temporal
# Nl = data['Nl']   # Número de cargas
# Ndl = data['Ndl'] # Número de cargas de referência
# Npv = data['Npv']  # Número de sistemas fotovoltaicos
# Nwt = data['Nwt']  # Número de sistemas de geração eólica

# p_l, p_pv, p_wt, p_dl_ref, p_dl_min, p_dl_max, tau_pld, tau_dist, tau_dl = projecoes(Nt, Nl, Ndl, Npv, Nwt)

# print(f'p_pl -> \nShape{p_l.shape}->\n {type(p_l)} -> \n{p_l}\n')
# print(f'p_pv -> \nShape{p_pv.shape}->\n {type(p_pv)} -> \n{p_pv}\n')
# print(f'p_wt -> \nShape{p_wt.shape}->\n {type(p_wt)} -> \n{p_wt}\n')
# print(f'p_dl_ref -> \nShape{p_dl_ref.shape}->\n{type(p_dl_ref)} -> \n{p_dl_ref}\n')
# print(f'p_dl_min -> \nShape{p_dl_min.shape}->\n{type(p_dl_min)} -> \n{p_dl_min}\n')
# print(f'p_dl_max -> \nSahpe{p_dl_max.shape}->\n{type(p_dl_max)} -> \n{p_dl_max}\n')
# print(f'tau_pld -> \nShape{tau_pld.shape}->\n{type(tau_pld)} -> \n{tau_pld}\n')
# print(f'tau_dist -> \nShape{tau_dist.shape}->\n{type(tau_dist)} -> \n{tau_dist}\n')
# print(f'tau_dl -> \nShape {tau_dl.shape}->\n{type(tau_dl)} -> \n{tau_dl}\n')

# for i in range(2):
#     plt.plot(p_l[i, :])
#     plt.plot(p_dl_ref[i,: ])
#     plt.plot(p_pv[i, :])
#     plt.title(f'Usina {i + 1}')
#     plt.xlabel('hora')
#     plt.ylabel('carga')
#     plt.legend(['p_l', 'p_dl', 'p_pv'])
#     plt.show()