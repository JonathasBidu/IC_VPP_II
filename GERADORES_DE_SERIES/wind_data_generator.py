import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt 
from WTGenPwr import WTGenPwr

''' SCRIPT PARA GERACAO DE SERIES DE VENTO A PARTIR DO CRESESB
    SUPOSICAO: VENTO TEM DISTRIBUICAO DE WEIBULL COM FATOR DE FORMA k e FATOR
    DE ESCALA C:
    f(v)=(k/C)(v/C)^(k-1)exp(-(v/C)^k) onde v eh a velocidade do vento e 
    f a funcao densidade de probabilidade de v.
'''

# definindo um intervalo em horas
while True:
    Npoints = input('Digite o intervalo de horas desejado ou tecle enter para 168 horas (1 semana) :')
    if Npoints == '':
        Npoints = 168
        break
    try:
        Npoints = int(Npoints)
        if Npoints > 0:
            Npoints = Npoints
            break
        else:
            print('Insira um valor numérrico válido')
    except ValueError:
        print('Insira um valor numérico válido')

# Definindo a quantidade de séries por usinas
while True:
    n = input('Insira a quantidade de séries ou tecle enter para 11: ')
    if n == '':
        n = 11
        break
    try:
        n = int(n)
        if n > 0:
            n = n
            break
        else:
            print('Insira um valor numérico válido!')
    except ValueError:
        print('Insira um valor numérico válido!')

#  Exemplo:
#   Para uma localização {Latitude:22,900223°  S, Longitude:43,125608° O}
#   o valor de C e k para cada periodo do ano são:
#       Periodo    |    C    |    k
#       Dez-Fev    |  5.07   |  1.82  
#       Mar-Mai    |  4.93   |  1.82
#       Jun-Ago    |  5.88   |  1.95
#       Set-Nov    |  5.22   |  1.90
#   Logo, pode-se adotar para scale e shape:
#       scale = [5.07;4.93;5.88;5.22]
#       shape = [1.82;1.82;1.95;1.90]

# Definir os parâmetros de distribuição de velocidade do vento
wind_hourly_series = np.zeros((n, Npoints))

# scale = input('Digite os fatores de escala c para cada trimestre do ano (ex: 5.07,4.93,5.88,5.22): ')
# shape = input('Digite os fatores de forma k para cada trimestre do ano (ex: 1.82,1.82,1.95,1.90): ')

# # Parâmetros padrão caso o usuário não forneça
# if not scale:
#     scale = [5.07, 4.93, 5.88, 5.22]
# else:
#     scale = list(map(float, scale.split(',')))

    # if not shape:
#     shape = [1.82, 1.82, 1.95, 1.90]
# else:
#     shape = list(map(float, shape.split(',')))
# Gerar séries temporais de velocidade do vento
        
scale = [5.07, 4.93, 5.88, 5.22]
shape = [1.82, 1.82, 1.95, 1.90]

dim1 = 1
dim2 = Npoints // 4  # total de horas do trimestre

for s in range(n):
    for trimestre in range(4):
        inicio = dim2 * trimestre
        fim = dim2 * (trimestre + 1)
        a = scale[trimestre]
        b = shape[trimestre]
        wind_hourly_series[s, inicio: fim] = stats.weibull_min.rvs(b, scale = a, size = dim2)

# # Parâmetros da eólica utilizados como padrão
# print('Parâmetros da UG Eólica')
# cut_in_speed = float(input('Velocidade de cut_in da turbina(m/s)[2.2]: ') or 2.2)
# cut_out_speed = float(input('Velocidade de cut_out da turbina(m/s)[25.0]: ') or 25.0)
# nom_speed = float(input('Velocidade nominal da turbina(m/s)[12.5]: ') or 12.5)
# nom_pwr = float(input('Potência nominal da turbina(W)[6000]: ') or 6000)
# Nwtg = int(input('Número de turbinas eólicas[1]: ') or 1)

# Parâmetros da eólica utilizados como padrão
cut_in_speed = 2.2
cut_out_speed = 25.0
nom_speed = 12.5
nom_pwr = 6000
Nwtg = 1

# Gerar séries temporais de potência eólica
WTGpwr_hourly_series = np.zeros_like(wind_hourly_series)
for s in range(n):
    for time in range(Npoints):
        speed = wind_hourly_series[s, time]
        Pwtg = WTGenPwr(speed, cut_in_speed, cut_out_speed, nom_speed, nom_pwr, Nwtg)
        WTGpwr_hourly_series[s, time] = Pwtg

# Salvar o DataFrame em um arquivo CSV, Excel ou outro formato
WTGpwr_hourly_series_df = pd.DataFrame(WTGpwr_hourly_series)
WTGpwr_hourly_series_df.to_csv("C:\\Users\\jonat\\OneDrive\\Área de Trabalho\\PROJETO_VPP_II\\SERIES_GERADAS\\WTGsystem_hourly_series.csv",
    sep=';',
    index = False,
    header = None
    )

for i in range(n):
    plt. figure(figsize = (12, 6))
    plt.title(f'Série eólica {i + 1}')
    plt. plot(WTGpwr_hourly_series_df.iloc[i, :])
    plt.xlabel('Hora')
    plt.ylabel('Carga')
    plt.show()