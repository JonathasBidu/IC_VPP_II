import numpy as np
from decomp_vetor_PO1 import decomp_vetor_x

'''
    Esta função contém as restrições do problema de 1° estágio.

    - Parâmetros:
        - x: vetor de variáveis
            - Atributos -> p_bm, u_bm e p_l
                - p_bm : potência das usinas de biomassa de dimensão (Nbm, Nt), onde, Nbm corresponde ao número de biomassa e Nt corresponde ao instante de tempo à frente.
                - u_bm : estado(ligado/desligado) das usinas de biomassa de dimensão (Nbm, Nt).
                - p_l : potência das cargas despachaveis de dimensão (Nl, Nt), onde, Nl corresponde a quantidade de cargas despachaveis.
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
                - c_bm : vetor contendo todas as retrições das usinas de biomassa.
                - c_dl : vetor contendo todas as restrições das cargas depachaveis.
'''

def const_PO1(x: np.ndarray, data: dict)-> np.ndarray:

    # Obtenção dos parâmetros individuais
    Nt = data['Nt']
    Nbm = data['Nbm']
    Ndl = data['Ndl']
    p_bm_min = data['p_bm_min']
    p_bm_max = data['p_bm_max']
    p_bm_rup = data['p_bm_rup']
    p_bm_rdown = data['p_bm_rdown']
    p_dl_max = data['p_dl_max']
    p_dl_min = data['p_dl_min']

    # Separção das variáveis no vetor solução
    p_bm, p_dl, u_bm, u_dl = decomp_vetor_x(x, Nt, Nbm, Ndl)

    # reshape de vetor em matrizes
    p_bm = p_bm.reshape((Nbm, Nt)) 
    u_bm = u_bm.reshape((Nbm, Nt))
    p_dl = p_dl.reshape((Ndl, Nt)) 
    u_dl = u_dl.reshape((Ndl, Nt))

    # Restrições da biomassa
    Nbmc = (Nt * Nbm) + (Nt * Nbm) + ((Nt - 1) * Nbm) + ((Nt - 1) * Nbm)
    c_bm = np.zeros(Nbmc)

    k = 0
    # p_bm_max (potência máxima da iésima usina de biomassa)
    for i in range(Nbm):
        for t in range(Nt):
            c_bm[k] = p_bm[i, t] - p_bm_max[i] * u_bm[i, t] 
            k += 1

    # p_bm_min (potência mínima da iésima usina de biomassa)
    for i in range(Nbm):
        for t in range(Nt):
            c_bm[k] = p_bm_min[i] * u_bm[i, t] - p_bm[i, t] 
            k += 1  

    # p_bm_rup (potência de rampa de subida)
    for i in range(Nbm):
        for t in range(1, Nt):
            c_bm[k] =  p_bm[i, t] - p_bm[i, t - 1] - p_bm_rup[i] 
            k += 1  

    # p_bm_rdown (potência de rampa de descida)
    for i in range(Nbm):
        for t in range(1, Nt):
            c_bm[k] = p_bm[i, t - 1] - p_bm[i, t] - p_bm_rdown[i] 
            k += 1

    # restrições das cargas despachaveis
    Ndlc = (Nt * Ndl) + (Nt * Ndl)
    c_dl = np.zeros(Ndlc)
    k = 0

    # p_dl_max (potência máxima da iésima carga despachavel)
    for i in range(Ndl):
        for t in range(Nt):
            c_dl[k] = p_dl[i, t] - p_dl_max[i, t] * u_dl[i, t]
            k +=1 

    # p_dl_min (potência mínima da iésima carga despachavel)
    for i in range(Ndl):
        for t in range(Nt):
            c_dl[k] = p_dl_min[i, t] * u_dl[i, t] - p_dl[i, t]

    # vetor contendo todas as restrições do PO1 (problema de primeiro estágio)
    c_ineq = np.concatenate((c_bm, c_dl))
   
    return c_ineq

# # Exemplo de uso:
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

    data['p_dl'] = p_dl_ref
    data['p_dl_max'] = p_dl_max
    data['p_dl_min'] = p_dl_min

    Nr = Nt * Nbm + Nt * Nl
    Ni = Nt * Nbm
    x = np.random.rand(Nr + Ni)

    constraints = const_PO1(x, data)

    print(f'Restrições do problema de primeiro estágio \n')
    print(f'O vetor de restrições do 1o estágio tem shape {constraints.shape} \n')
    print(constraints, '\n')
