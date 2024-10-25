import numpy as np
import pandas as pd
from pathlib import Path

'''
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
'''

def projecoes(Nt: int, Nl: int, Ndl: int, Npv: int, Nwt: int)-> tuple[np.ndarray, ...]:

    path = Path(__file__).parent.parent
    inicio = 0

    # carregamento das projeções das Cargas Não despacháveis
    path_1 = path / 'SERIES_GERADAS' / 'load_hourly_series.xlsx'
    files = pd.ExcelFile(path_1)
    p_l = np.zeros((Nl, Nt))

    for i, sheet in enumerate(files.sheet_names):

        load_hourly_series = pd.read_excel(path_1, header = None, sheet_name = sheet)
        m, _ = load_hourly_series.shape
        idx = np.random.choice(m)

        p_l[i, :] = load_hourly_series.iloc[idx, inicio: (inicio + Nt)].values / 1e6

    # carregamento das projeções das Cargas despacháveis
    path_2 = path / 'SERIES_GERADAS' / 'dload_hourly_series.xlsx'
    files = pd.ExcelFile(path_2)
    p_dl_ref = np.zeros((Ndl, Nt))

    for i, sheet in enumerate(files.sheet_names):

        dload_hourly_series = pd.read_excel(path_2, header = None, sheet_name = sheet)
        m, _ = dload_hourly_series.shape
        idx = np.random.choice(m)

        p_dl_ref[i, :] = dload_hourly_series.iloc[idx, inicio: (inicio + Nt)].values / 1e6

    # Carregamento das projeções das usinas solares
    path_3 = path / 'SERIES_GERADAS' / 'PVsystem_hourly_series.xlsx'
    files = pd.ExcelFile(path_3)
    p_pv = np.zeros((Npv, Nt))

    for i, sheet in enumerate(files.sheet_names):

        PVpwr_hourly_series = pd.read_excel(path_3, header = None, sheet_name = sheet)
        m, _ = PVpwr_hourly_series.shape
        idx = np.random.choice(m)

        p_pv[i, :] = PVpwr_hourly_series.iloc[idx,  inicio: (inicio + Nt)].values / 1e6

    # Carregamento das projeções das usinas éolicas
    path_4 = path / 'SERIES_GERADAS' / 'WTGsystem_hourly_series.xlsx'
    files = pd.ExcelFile(path_4)
    p_wt = np.zeros((Nwt, Nt))
    
    for i, sheet in enumerate(files.sheet_names):

        WTGsystem_hourly_series = pd.read_excel(path_4, header = None, sheet_name = sheet)
        m, _ = PVpwr_hourly_series.shape
        idx = np.random.choice(m)

        p_wt[i, :] = WTGsystem_hourly_series.iloc[idx,  inicio: (inicio + Nt)].values / 1e6

    # Carregamento das projeções de Preço de Liquidação de Diferença (PLD)
    path_5 = path / 'SERIES_GERADAS' / 'PLD_hourly_series.csv'
    PLD_hourly_series = pd.read_csv(path_5, sep = ';', header = None)
    m, _ = PLD_hourly_series.shape
    idx = np.random.choice(m)
    tau_pld = PLD_hourly_series.iloc[idx, inicio : (inicio + Nt)].values

    # Carregamento das projeções de tarifa da distribuidora
    path_6 = path / 'SERIES_GERADAS' / 'TDist_hourly_series.csv'
    TDist_hourly_series = pd.read_csv(path_6, sep = ';', header = None)
    m, _ = TDist_hourly_series.shape
    tau_dist = TDist_hourly_series.iloc[inicio : (inicio + Nt)].values
    tau_dl = 0.15 * TDist_hourly_series.iloc[inicio: (inicio + Nt)].values # Abatimento de 15% sobre o valor da tarifa

    dl_delta_min = np.zeros(int(Ndl))
    dl_delta_max = np.zeros(int(Ndl))

    for i in range(int(Ndl)):
        while True:
            dl_max = input(f'Insira o limite superior da carga {i + 1} ((%) acima da referência) ou tecle enter para 20%: ')
            if dl_max == '':
                dl_delta_max[i] = 20.0 # padrão de 20 por cento de limite de corte de carga superior
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

# Exemplos de uso
if __name__ == '__main__':

    import matplotlib.pyplot as plt
    from vpp_data import vpp

    data = vpp()

    Nt = 24  # Número de pontos de dados na série temporal
    Nl = data['Nl']   # Número de cargas
    Ndl = data['Ndl'] # Número de cargas de referência
    Npv = data['Npv']  # Número de sistemas fotovoltaicos
    Nwt = data['Nwt']  # Número de sistemas de geração eólica

   

    p_l, p_pv, p_wt, p_dl_ref, p_dl_min, p_dl_max, tau_pld, tau_dist, tau_dl = projecoes(Nt, Nl, Ndl, Npv, Nwt)

    # plot das projeções de cargas Não despacháveis
    for i in range(Nl):

        title = f'Carga NÃO Despachável {i + 1}'
        plt.figure(figsize = (10, 4))
        plt.title(title)
        plt.plot(p_l[i, :], 'r')
        plt.xlabel('hora')
        plt.ylabel('potência em MW')
        plt.show()

    # plot das sérieprojeções de cargas despacháveis de referência, mínima e máxima
    for i in range(Ndl):

        title = f'Carga Despachável {i + 1}'
        plt.figure(figsize = (10, 4))
        plt.title(title)
        plt.plot(p_dl_ref[i, :], 'k')
        plt.plot(p_dl_min[i, :], 'b--')
        plt.plot(p_dl_max[i, :], 'b--')
        plt.legend(['ref', 'min', 'max'])
        plt.xlabel('hora')
        plt.ylabel('potência em MW')
        plt.show()

    # plot da projeções das usinas solares
    for i in range(Npv):

        title = f'Usina Solar {i + 1}'
        plt.figure(figsize = (10, 4))
        plt.title(title)
        plt.plot(p_pv[i, :], 'r')
        plt.xlabel('hora')
        plt.ylabel('potência em MW')
        plt.show()
   
    # plot da projeções das usinas éolicas
    for i in range(Npv):

        title = f'Usina Eólica {i + 1}'
        plt.figure(figsize = (10, 4))
        plt.title(title)
        plt.plot(p_wt[i, :], 'r')
        plt.xlabel('hora')
        plt.ylabel('potência em MW')
        plt.show()

    # Plotagem das projeções de PLD
    plt.figure(figsize = (10, 4))
    plt.title('Preço de Liquidação de Diferença')
    plt.plot(tau_pld)
    plt.show()
    
    # Plotagem da projeção da Tarifa da distribuição e da compensação para o usuário
    plt.figure(figsize = (10, 4))
    plt.title('Tarifa da Distribuição e Compensação')
    plt.plot(tau_dist[0, :Nt], 'b')
    plt.plot(tau_dl[0, :Nt], 'r')
    plt.legend(['Dist', 'Desc 15%'])
    plt.show()
