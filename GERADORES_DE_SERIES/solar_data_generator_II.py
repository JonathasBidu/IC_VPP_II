import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Importar os dados do Excel
path = 'C:\\Users\\Jonathas Aguiar\\Desktop\\IC_VPP_II\\GERADORES_DE_SERIES\\BASE_DE_DADOS\\Atlas_Global_Solar.xlsx'
atlas_df = pd.read_excel(path, header = None)

# Supondo que os dados estejam em formato (24, 12)
media_mensal = atlas_df.values

# Transpor os dados para que as horas sejam nas linhas e os meses nas colunas
media_mensal = media_mensal.T

# Criar a série temporal de 8760 horas
solar_tsdata = np.zeros(8760)

# Preencher a série temporal com médias mensais
for mes in range(12):
    inicio = mes * 720  # 30 dias x 24 horas = 720 horas
    fim = (mes + 1) * 720
    # Repetir as médias diárias para preencher 30 dias
    solar_tsdata[inicio: fim] = np.tile(media_mensal[mes, :], 30)

# Adicionar ruído gaussiano
def gerar_ruido_diario(amplitude, num_dias):
    return np.random.normal(loc = 0, scale = amplitude, size = (num_dias, 24))

# Número de dias (365 dias)
num_dias = 365
amplitude_ruido = 25 # Ajuste a amplitude do ruído conforme necessário

# Gerar ruído para cada dia do ano
ruido_diario = gerar_ruido_diario(amplitude_ruido, num_dias)

# Adicionar o ruído à série temporal
PVpwr_hourly_series = np.copy(solar_tsdata)

# Adicionar ruído apenas onde a potência é maior que zero
for dia in range(num_dias):
    inicio = dia * 24
    fim = (dia + 1) * 24
    mask = solar_tsdata[inicio: fim] > 0
    PVpwr_hourly_series[inicio: fim][mask] += ruido_diario[dia][mask]

# Garantir que os valores não sejam negativos
PVpwr_hourly_series = np.clip(PVpwr_hourly_series, a_min = 0, a_max = None)

# Arredondar valores para inteiros
PVpwr_hourly_series = np.round(PVpwr_hourly_series).astype(int)

print(PVpwr_hourly_series.shape)
plt.figure(figsize = (10, 4))
plt.plot(PVpwr_hourly_series[: 96])
plt.show()

