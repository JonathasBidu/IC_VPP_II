from decomp_vetor_PO2 import decomp_vetor_y
import numpy as np

def custo_PO2(x, Cbm, data):

    Nt = data['Nt']
    Nbm = data['Nbm']  
    Ndl = data['Ndl']
    Nl = data['Nl']
    Npv = data['Npv']
    Nwt = data['Nwt']
    Nbat = data['Nbat']
    tau_pld = data['tau_pld']
    tau_dl = data['tau_dl']
    tau_dist = data['tau_dist']
    kappa_bm = data['kappa_bm']
    kappa_bm_start = data['kappa_bm_start']
    kappa_pv = data['kappa_pv']
    kappa_wt = data['kappa_wt']
    kappa_bat = data['kappa_bat']
    p_pv = data['p_pv']
    p_l = data['p_l']
    p_wt = data['p_wt']

    # decompor o vetor x (variaveis de controle do 1o estagio)
    #p_bm, u_bm = decomp_vetor(x, Nt, Nbm)

    #p_bm, p_dl, p_chg, p_dch, soc, u_bm,u_dl, u_chg, u_dch = decomp_vetor_PO2(x, Nbm, Nt, Ndl, Nbat) errado
    #p_bm, p_dl, p_chg, p_dch, soc, u_bm,u_dl, u_chg, u_dch = decomp_vetor_PO2(y, Nbm, Nt, Ndl, Nbat) certo
    
    # p_bm = p_bm.reshape((Nbm, Nt))
    # p_dl = p_dl.reshape((Ndl, Nt))
    # p_chg = p_chg.reshape((Nbat, Nt))
    # p_dch = p_dch.reshape((Nbat, Nt))
    # soc = soc.reshape((Nbat, Nt))
    # u_bm = u_bm.reshape((Nbm, Nt))
    # u_dl = u_dl.reshape((Nbat, Nt))
    # u_chg = u_chg.reshape((Nbat, Nt))
    # u_dch = u_dch.reshape((Nbat, Nt))
 
    # # Despesa total
    # D = D + Cpv + Cwt + Cbm + Cdl + Cbat
    # Função objetivo do problema 2
    # fval = R - D
    
    
    
    
    
    
    # for s in Ncenarios:
        # carregar o cenario s em  p_pv, p_wt e p_l
    # Lucro
        # atualizar a funcao objetivo PO2
        # lambda: [variavrid] func_PO2(x, data, s)
        # atualizar a funcao de restricoes PO2 
        # chamar o otimizador do problema PO2
        # obter a solicao otima de PO2
        #calcular func_PO2 para a solucao otima
        #armazena num vetor de custo otimo

    #calcular a media dos custos otimos    
    # fval = # custo otimo medio

    return ...
