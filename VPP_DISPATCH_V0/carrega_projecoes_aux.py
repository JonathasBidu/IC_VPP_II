import numpy as np
import pandas as pd

def carrega(Nt: int|None, Nl: int|None, Ndl: int|None, Npv: int|None, Nwt: int|None)-> tuple[np.ndarray, ...]:

    inicio = 0

    path_1 = "C:\\Users\\Jonathas Aguiar\\Desktop\\IC_VPP_II\\SERIES_GERADAS\\dload_hourly_series.xlsx"
    
    files = pd.ExcelFile(path_1)
    p_l = np.zeros(Ndl, Nt)

    for i, sheet in enumerate(files.sheet_names):

        dload_hourly_series = pd.read_excel(path_1, header = None, sheet_name = sheet)

        m, _ = dload_hourly_series.shape
        idx = np.random.choice(m, 1)

        p_l[i, :] = dload_hourly_series.iloc[idx, inicio: (inicio + Nt)].values




    return p_l

Nt = 24
Ndl = 3

p_l = carrega(Nt, Nl = None, Ndl, Npv = None)