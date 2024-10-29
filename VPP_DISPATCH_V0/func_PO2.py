from decomp_vetor_PO2 import decomp_vetor_y
import numpy as np

def func_PO2(y, data):

    # Obtenção dos parâmetros individuais
    Nt = data['Nt']
    Ndl = data['Ndl']
    Nbat = data['Nbat']
    Nl = data['Nl']
    Npv = data['Npv']
    Nwt = data['Nwt']
    kappa_pv = data['kappa_pv']
    kappa_wt = data['kappa_wt']
    kappa_bat = data['kappa_bat']
    p_pv = data['p_pv']
    p_wt = data['p_wt']
    p_l = data['p_l']
    tau_pld = data['tau_pld']
    tau_dist = data['tau_dist']
    tau_dl = data['tau_dl']    

    # Separção das variáveis no vetor solução y
    p_chg, p_dch, soc, u_chg, u_dch = decomp_vetor_y(y, Nt, Ndl, Nbat)

    # reshape de vetor em matrizes
    p_dl = p_dl.reshape((Ndl, Nt))
    p_chg = p_chg.reshape((Nbat, Nt))
    p_dch = p_dch.reshape((Nbat, Nt))
    soc = soc.reshape((Nbat, Nt))
    u_dl = u_dl.reshape((Ndl, Nt))
    u_chg = u_chg.reshape((Nbat, Nt))
    u_dch = u_dch.reshape((Nbat, Nt))

    # potência líquida
    p_liq = np.zeros(Nt)
    for t in range(Nt):
        for i in range(Npv):
            p_liq[t] += p_pv[i, t]
        for i in range(Nwt):
            p_liq[t] += p_wt[i, t]
        for i in range(Nl):
            p_liq[t] -= p_l[i, t]
        for i in range(Ndl):
            p_liq[t] -= p_dl[i, t] * u_dl[i, t]
        for i in range(Nbat):
            p_liq[t] -= p_chg[i, t] * u_chg[i, t] + p_dch[i, t] * u_dch[i, t]

    p_exp = np.maximum(0, p_liq)
    p_imp = np.maximum(0, - p_liq)

    # Receita com excedente de energia
    R = 0
    for t in range(Nt):
        R += p_exp[t] * tau_pld[t]

    # Despesa com importação de energia
    D = 0
    for t in range(Nt):
        D += p_imp[t] * tau_dist[t]

    # Custo da geração fotovoltaica
    Cpv = 0
    for t in range(Nt):
        for i in range(Npv):
            Cpv += p_pv[i, t] * kappa_pv[i]

    # Custo da geração eólica
    Cwt = 0
    for t in range(Nt):
        for i in range(Nwt):
            Cwt += p_wt[i, t] * kappa_wt[i]
    
    # Custo de controle de carga despachada
    Cdl = 0 
    for t in range(Nt):
        for i in range(Ndl):
            Cdl += p_dl[i, t] * u_dl[i, t] * tau_dl[t]

    # Custo da bateria
    Cbat = 0 
    for t in range(Nt):
        for i in range(Nbat):
            Cbat += ((p_chg[i, t] * u_chg[i, t] + p_dch[i, t] * u_dch[i, t]) * kappa_bat[i])

    D = D + Cpv + Cwt + Cdl + Cbat

    fval = R - D

    return fval

# # Exemplo de uso:
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
# Nbm = data['Nbm']

# p_l, p_pv, p_wt, p_dl_ref, p_dl_min, p_dl_max, tau_pld, tau_dist, tau_dl = projecoes(Nt, Nl, Ndl, Npv, Nwt)

# kappa_pv = data['kappa_pv']
# kappa_wt = data['kappa_wt']
# kappa_bat = data['kappa_bat']
# data['p_pv'] = p_pv
# data['p_wt'] = p_wt
# data['p_l'] = p_l
# data['tau_pld'] = tau_pld
# data['tau_dist'] = tau_dist
# data['tau_dl'] = tau_dl

# # Quantidade de variaveis em y
# Nr = (Nt * Ndl) + (Nt * Nbat) + (Nbat * Nt) + (Nbat * Nt)
# Ni = (Nt * Ndl) + (Nbat * Nt) + (Nbat * Nt)
# # gerando um vetor de teste y
# y = np.random.rand(Nr + Ni)

# # obtendo as variaveis do vetor epsolon
# data['p_dl_min'] = p_dl_min
# data['p_dl_max'] = p_dl_max

# f = func_PO2(y, data)

# print(f'{f:.2f}')
