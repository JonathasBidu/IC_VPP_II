import numpy as np
from decomp_vetor_PO2 import decomp_vetor_PO2
'''
    Esta função contém as restrições do problema de 1° estágio.

    - Parâmetros:
        - vetor y:
            - Atributos -> p_bm, u_bm e p_l
                - p_bat : potência dos armazenadores de dimensão (Nbat, Nt), onde, Nbat corresponde ao número de baterias e Nt corresponde ao instante de tempo à frente.
                - p_dl : potência das cargas não despachaveis de dimensão (Ndl, Nt), onde, Ndl é a quantidade de cargas não despachaveis.
                - u_dch : estado(ligado/deligado) de descarga da bateria.
                - u_chg : estado(ligado/deligado) de carga da bateria.
        - data : dicionário contendo parâmetros iniciais da vpp.
            - Atributos:
                - Nbm : quantidade de usinas de biomassa.
                - Ndl : quantidade de cargas não despachaveis.
                - Nl : quantidade de cargas despachaveis.
                - Npv : quantidade de usinas fotovoltaicas.
                - Nwt : quantidade de usinas eólicas.
                - Nbat : quantidade de armazenadores.
                - p_bm_min : potência mínima das usinas de biomassa.
                - p_bm_max : potência máxima das usinas de biomassa.
                - p_bm_rup : potência de subida das usina de biomassa.
                - p_bm_rdown : potência de descida das usinas de biomassa.
                - kappa_bm : preço de custo operciaonal das usinas de biomassa.
                - kappa_bm_start : preço de custo de partida das usinas de biomassa.
                - kappa_pv : preço de custo operacional das usinas fotovoltaicas.
                - kappa_wt : preço de custo operacional das usinas eólicas.
                - kappa_bat : preço de custo opercional dos armazenadores.
                - soc_min : balanço mínimo dos armazenadores.
                - soc_max : balanço máximo dos armazenadores.
                - eta_chg : rendimento da carga da bateria.
                - eta_dch : rendimento da descarga da bateria.
                - p_bat_max : potência máxima suportada pelos armazenadores.

    - Retorna: 
        - c_ineq:
            - Atributos:
                - c_bat : vetor contendo todas as retrições dos armazenadores.
                - c_dl : vetor contendo todas as retrições das cargas não despachaveis.

'''

def const_PO2(y, data: dict):

    # Obtenção dos parâmetros individuais
    Nt = data['Nt']
    Nbat = data['Nbat']
    eta_chg = data['eta_chg']
    eta_dch = data['eta_dch']
    p_bat_max = data['p_bat_max']

    # Separção das variáveis no vetor solução
    p_chg, p_dch, soc, u_chg, u_dch = decomp_vetor_PO2(y, Nt, Nbat)

    # reshape de vetrore em matrizes
    p_chg = p_chg.reshape((Nbat, Nt))
    p_dch = p_dch.reshape((Nbat, Nt))
    soc = soc.reshape((Nbat, Nt))
    u_chg = u_chg.reshape((Nbat, Nt))
    u_dch = u_dch.reshape((Nbat, Nt))

    # Restrições da bateria
    Nbatc = ((Nt - 1) * Nbat) + ((Nt - 1) * Nbat) + (Nt*Nbat) + (Nt*Nbat) + (Nt*Nbat)
    c_bat = np.zeros(Nbatc)
    k = 0

    # soc balanço +
    for i in range(Nbat):
        for t in range(1, Nt):
            c_bat[k] = soc[i, t] - soc[i, t - 1] - p_chg[i, t] * eta_chg[i] + p_dch[i, t] / eta_dch[i]
            k += 1

    # soc balanço -
    shift = ((Nt - 1) * Nbat)
    for i in range(Nbat):
        for t in range(1, Nt):
            c_bat[k] = - c_bat[k - shift]
            k += 1

    # limites máximo descarga
    for i in range(Nbat):
        for t in range(Nt):
            c_bat[k] = p_dch[i, t] - p_bat_max[i] * u_dch[i, t]
            k += 1

    # limites de simultaneidade de carga e descarga
    for i in range(Nbat):
        for t in range(Nt):
            c_bat[k] = u_chg[i, t] + u_dch[i, t] - 1 # conferido (ok)
            k += 1


    c_ineq = c_bat
   
    return c_ineq  

# # Array de teste
# from vpp_data import vpp
# from carrega_projecoes import projecoes


# data = vpp()

# Nt = 24 # Número de instantes de tempo a frente
# data['Nt'] = Nt
# Ndl = 3 # Número de cargas despacháveis
# Nbat = 4 # Número de bateria
# Nl = data['Nl']
# Ndl = data['Ndl']
# Nwt = data['Nwt']
# Npv = data['Npv']
# Nr = (Nt * Ndl) + (Nt * Nbat) + (Nbat * Nt) + (Nbat * Nt)
# Ni = (Nt * Ndl) + (Nbat * Nt) + (Nbat * Nt)
# p_l, p_pv, p_wt, p_dl_ref, p_dl_min, p_dl_max, tau_pld, tau_dist, tau_dl = projecoes(Nt, Nl, Ndl, Npv, Nwt)

# data['p_dl_min'] = p_dl_min
# data['p_dl_max'] = p_dl_max

# y = np.random.rand(Nr + Ni)

# c = const_PO2(y, data)

# print(c, f' o tipo é c{type(c)} e o  seu shape é {c.shape}','\n')