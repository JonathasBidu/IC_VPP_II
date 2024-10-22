import numpy as np
import pandas as pd
from pathlib import Path

def projecoes(Nt: int, Nl: int, Ndl: int, Npv: int, Nwt: int)-> tuple[np.ndarray, ...]:

    path = Path(__file__).parent.parent
    # c:\Users\jonat\OneDrive\Área de Trabalho\PROJETO_VPP_II

    inicio = 0

    # Cargas despacháveis
    # path_1 = "C:\\Users\\Jonathas Aguiar\\Desktop\\IC_VPP_II\\SERIES_GERADAS\\dload_hourly_series.xlsx"
    path_1 = path / 'SERIES_GERADAS' / 'dload_hourly_series.xlsx'
    files = pd.ExcelFile(path_1)
    p_l = np.zeros((Ndl, Nt))

    for i, sheet in enumerate(files.sheet_names):

        dload_hourly_series = pd.read_excel(path_1, header = None, sheet_name = sheet)

        m, _ = dload_hourly_series.shape
        idx = np.random.choice(m, 1)

        p_l[i, :] = dload_hourly_series.iloc[idx, inicio: (inicio + Nt)].values / 1e6

    # Carregamento das séries de potência das usinas solares
    # path_2 = 'C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP_II\\SERIES_GERADAS\\PVsystem_hourly_series.xlsx'
    path_2 = path / 'SERIES_GERADAS' / 'PVsystem_hourly_series.xlsx'

    files = pd.ExcelFile(path_2)
    p_pv = np.zeros((Npv, Nt))

    for i, sheet in enumerate(files.sheet_names):

        PVpwr_hourly_series = pd.read_excel(path_2, header = None, sheet_name = sheet)
        m, _ = PVpwr_hourly_series.shape
        idx = np.random.choice(m, 1)

        p_pv[i, :] = PVpwr_hourly_series.iloc[idx,  inicio: (inicio + Nt)].values / 1e6


    return p_l, p_pv

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

   

    p_l, p_pv = projecoes(Nt, Nl, Ndl, Npv, Nwt)

    # plot das séries de potência das cargas despacháveis
    for i in range(Ndl):

        title = f'Carga Despachável {i + 1}'
        plt.figure(figsize = (10, 4))
        plt.title(title)
        plt.plot(p_l[i, :], 'r')
        plt.xlabel('hora')
        plt.ylabel('potência em MW')
        plt.show()
   
    # plot das séries de potência das usinas solares
    for i in range(Npv):

        title = f'Usina Solar{i + 1}'
        plt.figure(figsize = (10, 4))
        plt.title(title)
        plt.plot(p_pv[i, :], 'r')
        plt.xlabel('hora')
        plt.ylabel('potência em MW')
        plt.show()
   
