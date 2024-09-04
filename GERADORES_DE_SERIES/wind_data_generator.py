import numpy as np
import scipy.stats as stats
from WTGenPwr import WTGenPwr

''' SCRIPT PARA GERACAO DE SERIES DE VENTO A PARTIR DO CRESESB
    SUPOSICAO: VENTO TEM DISTRIBUICAO DE WEIBULL COM FATOR DE FORMA k e FATOR
    DE ESCALA C:
    f(v)=(k/C)(v/C)^(k-1)exp(-(v/C)^k) onde v eh a velocidade do vento e 
    f a funcao densidade de probabilidade de v.
'''

def wind_data_generation():
        
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

    scale = []
    shape = []

    for i in range(4):
        while True:
            c = input(f'Insira o fator C do {i+1}° trimestre: ')
            try:
                c = float(c)
                if c > 0:
                    break
                else:
                    print('Insira um valor real positivo')
            except ValueError as v:
                print(f'Insira um valor real positivo!\nErro, {v}')
        while True:
            k = input(f'Insira o fator K do {i+1}° trimestre ')
            try:
                k = float(k)
                if k > 0:
                    break
                else:
                    print('Insira um valor real positivo')
            except ValueError as v:
                print(f'Insira um valor real positivo!\nErro, {v}')
        scale.append(c)
        shape.append(k)


    dim1 = 1
    dim2 = Npoints // 4  # total de horas do trimestre

    for s in range(n):
        for trimestre in range(4):
            inicio = dim2 * trimestre
            fim = dim2 * (trimestre + 1)
            a = scale[trimestre]
            b = shape[trimestre]
            wind_hourly_series[s, inicio: fim] = stats.weibull_min.rvs(b, scale = a, size = dim2)

#     # # Parâmetros da eólica utilizados como padrão
#     # print('Parâmetros da UG Eólica')
#     # cut_in_speed = float(input('Velocidade de cut_in da turbina(m/s)[2.2]: ') or 2.2)
#     # cut_out_speed = float(input('Velocidade de cut_out da turbina(m/s)[25.0]: ') or 25.0)
#     # nom_speed = float(input('Velocidade nominal da turbina(m/s)[12.5]: ') or 12.5)
#     # nom_pwr = float(input('Potência nominal da turbina(W)[6000]: ') or 6000)
#     # Nwtg = int(input('Número de turbinas eólicas[1]: ') or 1)

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

    return WTGpwr_hourly_series

if __name__ == '__main__':

    import pandas as pd
    from pathlib import Path
    
    while True:
        Nwt = input('Digite a quantidade de usinas desejadas ou tecle enter para 3: ')
        if Nwt == '':
            Nwt = 3
            break
        try:
            Nwt = int(Nwt)
            if Nwt > 0:
                break
            else:
                print('Insira um valor numérico válido')
        except ValueError as v:
            print(f'Insira um valor numérico válido\nERRO, {v}')

    save_path = Path(__file__).parent.parent / 'SERIES_GERADAS' / 'WTGsystem_hourly_series.xlsx'

    with pd.ExcelWriter(save_path) as writer:
        for i in  range(Nwt):
            WTG_horly_series = wind_data_generation()
            WTG_horly_series_df = pd.DataFrame(WTG_horly_series)
            WTG_horly_series_df.to_excel(writer, sheet_name = f'Usina {i + 1}', header = None, index = False)
    
    print('FIM')
