from decomp_vetor_PO2 import decomp_vetor_y

import numpy as np

def func(y, data):

    Nt = data['Nt']
    Nbat = data['Nbat']
    Nl = data['Nl']
    Npv = data['Npv']
    Nwt = data['Nwt']
    kappa_pv = data['kappa_pv']
    kappa_wt = data['kappa_pv']
    kappa_bat = data['kappa_bat']
    tau_dist = data['tau_dist']
    tau_pld = data['tau_pld']
    p_pv = data['p_pv']
    p_wt = data['p_wt']
    p_l = data['p_l']


    p_chg, p_dch, soc, u_chg, u_dch = decomp_vetor_y(y, Nt, Nbat)

    # Reshape dos vetores em matrizes
    p_chg = p_chg.reshape((Nbat, Nt))
    p_dch = p_dch.reshape((Nbat, Nt))
    soc = soc.reshape((Nbat, Nt))
    u_chg = u_chg.reshape((Nbat, Nt))
    u_dch = u_dch.reshape((Nbat, Nt))
  
  
    # Cálculo da potência líquida
    p_liq = np.zeros(Nt)

    for t in range(Nt):
        for i in range(Npv):
            p_liq[t] += p_pv[i, t]
        for i in range(Nwt):
            p_liq[t] += p_wt[i, t]
        for i in range(Nl):
            p_liq[t] -= p_l[i, t]
        for i in range(Nbat):
            p_liq[t] -= p_chg[i, t] * u_chg[i, t] + p_chg[i, t] * u_chg[i, t]
        

    p_exp = np.maximum(0, p_liq)
    p_imp = np.maximum(0, - p_liq)

    # Receita com excedente de energia
    R = 0
    for t in range(Nt):
        R += p_exp[t] * tau_pld[t]

    # Despesa com importação de energia
    D = 0

    # Importação de energia da distribuidora
    for t in range(Nt):
        D += p_imp[t] * tau_dist[t]

    # Custos de geração biomassa (custo linear)
    Cpv = 0
    for t in range(Nt):
        for i in range(Npv):
            Cpv += p_pv[i, t] * kappa_pv[i]

    # Custo da geração Eólica
    Cwt = 0
    for t in range(Nt):
        for i in range(Nwt):
            Cwt += p_wt[i, t] * kappa_wt[i]

    Cbat = 0
    for t in range(Nt):
        for i in range(Nbat):
            Cbat += ((p_chg[i, t] * u_chg[i, t] + p_dch[i, t] * u_dch[i, t]) * kappa_bat[i])

    D = D + Cwt + Cpv + Cbat

    fval = R - D

    return fval

if __name__ == '__main__':

    from vpp_data import vpp
    from carrega_projecoes import projecoes

    data = vpp()

    Nt = 24
    data['Nt'] = Nt
    Nbm = data['Nbm']
    Nl = data['Nl']
    Ndl = data['Ndl']
    Npv = data['Npv']
    Nwt = data['Nwt']
    Nbat = data['Nbat']

    p_l, p_pv, p_wt, p_dl_ref, p_dl_min, p_dl_max, tau_pld, tau_dist, tau_dl = projecoes(Nt, Nl, Ndl, Npv, Nwt)

    data['tau_dl'] = tau_dl
    data['tau_dist'] = tau_dist
    data['tau_pld'] = tau_pld
    data['p_pv'] = p_pv
    data['p_wt'] = p_wt
    data['p_l'] = p_l

    Nr = (Nbat * Nt) + (Nbat * Nt) + (Nbat * Nt)
    Ni = (Nbat * Nt) + (Nbat * Nt) 
    y = np.random.rand(Nr + Ni)

    func = func(y, data)

    print('Vizualizão da função objetivo do problema de segundo estágio \n')
    print(func)
    print(type(func))
