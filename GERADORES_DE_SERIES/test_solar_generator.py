import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PVGenPwr import PVGenPwr

path = 'C:\\Users\\Jonathas Aguiar\\Desktop\\IC_VPP_II\\GERADORES_DE_SERIES\\BASE_DE_DADOS\\solar_hourly_series.xlsx'

sheets = pd.ExcelFile(path)

print(sheets. sheet_names)


# while True:
#     Npoints = input('Insira o intervalo em horas desejado ou tecle enter para 168 horas(1 semana): ')
#     if Npoints == '':
#         Npoints = 168
#         break
#     try:
#         Npoints = int(Npoints)
#         if Npoints > 0:
#             Npoints = Npoints
#             break
#         else:
#             print('Digite um valor numérico válido')
#     except ValueError:
#         print('Digite um valor numérico válido')

# while True:
#     n = input('Digite a quantidade de séries desejada ou tecle enter para 11: ')
#     if n == '':
#         n = 11
#         break
#     try:
#         n = int(n)
#         if n > 0:
#             n = n
#             break
#         else:
#             print('Insira um valor numérico válido')
#     except ValueError:
#         print('insira um valor numérico válido') 

for i in sheets.sheet_names:
    print(i)
# irradiance_hourly_series = np.zeros((n, Npoints))
# temperature_hourly_series = np.zeros((n, Npoints))

# # quantidade de módulos em paralelo
# Np = 400
# # quantidade de módulos em série
# Ns = 2000

# for i in range(n):
#     inicio = Npoints * i
#     fim = Npoints * (i+1)
#     irradiance_hourly_series[i, :] = solar_tsdata.iloc[inicio: fim, 0].values
#     temperature_hourly_series[i, :] = solar_tsdata.iloc[inicio: fim, 1].values

# PVpwr_irradiance_hourly_series = np.zeros_like(irradiance_hourly_series)

# # Iterar sobre cenários e pontos no tempo
# for s in range(n):
#     for time in range(Npoints):
#         T = temperature_hourly_series[s, time] + 20 + 273.15  # graus Kelvin
#         T += 25.00  # Adicionando ajuste temporário
#         G = irradiance_hourly_series[s, time]
#         Pmmp, Vmmp, Immp = PVGenPwr(G, T, Np, Ns)
#         PVpwr_irradiance_hourly_series[s, time] = Pmmp
#         print(s, time)
# print(fim)

# # salvamento da série em um arquivo csv
# PVpwr_hourly_series_pd = pd.DataFrame(PVpwr_irradiance_hourly_series)
# PVpwr_hourly_series_pd.to_csv('C:\Users\Jonathas Aguiar\Desktop\IC_VPP_II\SERIES_GERADAS\PVsystem_hourly_series.csv', sep = ';', index = False, header = None)

# for i in range(n):
#     plt.figure(figsize = (12, 5))
#     plt.title(f'Série FV {i + 1}')
#     plt.plot(PVpwr_hourly_series_pd.iloc[i,:], 'r')
#     plt.xlabel('Hora')
#     plt.ylabel('Carga')
#     plt.show()

