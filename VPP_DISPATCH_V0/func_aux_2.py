from decomp_vetor_PO2 import decomp_vetor_y

import numpy as np

def func(y, data):

    Nt = data['Nt']
    Nbm = data['Nbm']
    Ndl = data['Ndl']
    kappa_bm = data['kappa_bm']
    kappa_bm_start = data['kappa_bm_start']
    tau_dl = data['tau_dl']
    tau_dist = data['tau_dist']
    tau_pld = data['tau_pld']


    p_bm, p_dl, u_bm, u_dl = decomp_vetor_y(y, Nt, Nbm, Ndl)

    p_bm = p_bm.reshape((Nbm, Nt))
    p_dl = p_dl.reshape((Ndl, Nt))
    u_bm = u_bm.reshape((Nbm, Nt))
    u_dl = u_dl.reshape((Nbm, Nt))


    p_liq = np.zeros(Nt)
    for t in range(Nt):
        for i in range(Nbm):
            p_liq[t] += p_bm[i, t]
        for i in range(Ndl):
            p_liq[t] += p_dl[i, t]

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

    # Custos de geração biomassa (custo linear)
    Cbm = 0
    for t in range(Nt):
        for i in range(Nbm):
            Cbm += p_bm[i, t] * u_bm[i, t] * kappa_bm[i]
    
    #  custo de partida
    for t in range(1, Nt):
        for i in range(Nbm):
            Cbm += (u_bm[i, t] - u_bm[i, t - 1]) * kappa_bm_start[i]

    # Custo de controle de carga despachada
    Cdl = 0
    for t in range(Nt):
        for i in range(Ndl):
            Cdl += p_dl[i, t] * u_dl[i, t] * tau_dl[t]

    D = D + Cdl + Cbm

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

    p_l, p_pv, p_wt, p_dl_ref, p_dl_min, p_dl_max, tau_pld, tau_dist, tau_dl = projecoes(Nt, Nl, Ndl, Npv, Nwt)

    data['tau_dl'] = tau_dl
    data['tau_dist'] = tau_dist
    data['tau_pld'] = tau_pld

    Nr = Nt * Nbm + Nt * Ndl
    Ni = Nt * Nbm + Nt * Ndl
    x = np.random.rand(Nr + Ni)

    func = func(x, data)

    print('Vizualizão da função objetivo do problema de primeiro estágio \n')
    print(func)
    print(type(func))
