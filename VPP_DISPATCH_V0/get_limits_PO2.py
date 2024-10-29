import numpy as np

"""
    Esta função constrói o vetor de limites para a VPP descrita em VPP data

    Parâmetros:
    - vpp_data: Dicionário contendo os parametros da VPP. possui os seguintes atributos:

        - Nt: número de instantes de simulação
        - Nbm: número de usinas biomassa
        - Ndl: número de cargas despacháveis
        - Nbat: número de baterias
        - Nwt: número de geradores eólicos
        - Npv: número de usinas solares
        - p_l: potência das cargas, dimensão ((Nl*Nt), 1)
        - p_pv: potência das UG solares FV, dimensão ((Npv*Nt), 1)
        - p_wt: potência das UG eólicas, dimensão ((Nwt*Nt), 1)
        - p_bm_min: potência mínima biomassa, dimensão (Nbm, 1)
        - p_bm_max: potência máxima biomassa, dimensão (Nbm, 1)
        - p_bm_rup: potência máxima ramp up biomassa, dimensão (Nbm, 1)
        - p_bm_rdown: potência máxima ramp down biomassa, dimensão (Nbm, 1)
        - eta_chg: rendimento carga bateria, dimensão (Nbat, 1)
        - eta_dch: rendimento descarga bateria, dimensão (Nbat, 1)
        - soc_min: SoC mínimo bateria, dimensão (Nbat, 1)
        - soc_max: SoC máximo bateria, dimensão (Nbat, 1)
        - p_bat_max: potência máxima carga/descarga bateria, dimensão (Nbat, 1)
        - p_dl_min: potência mínima despachável carga, dimensão (Ndl, 1)
        - p_dl_max: potência máxima despachável carga, dimensão (Ndl, 1)
        - tau_dl: compensação por corte, dimensão (Ndl, 1)
        - tau_pld: PLD, dimensão (Nt, 1)
        - tau_dist: tarifa distribuidora
        - kappa_pv: custo unitário ger. solar
        - kappa_wt: custo unitário ger. eólica
        - kappa_bm: custo unitário ger. biomassa
        - kappa_bm_start: custo unitário partida ger. biomassa
        - kappa_bat: custo baterias

    Retorna:
        - Uma tupla contendo dois vetores que limitam...
            - lb: vetor limite inferior das variáveis de decisão
            - ub: vetor limite superior das variáveis de decisão

"""

def vpplimits_PO2(data):

    Nt = int(data['Nt'])
    Nbat = int(data['Nbat'])

    # Obtencao dos paramteros da VPP
    Nr = (Nbat * Nt) + (Nbat * Nt) + (Nbat * Nt)
    Ni = (Nbat * Nt) + (Nbat * Nt)

    #  Criação lb e ub
    # nvars -> Qtd de variáveis
    nvars = Nr + Ni
    lb = np.zeros(nvars) 
    ub = np.ones(nvars) 

    # limtes de p_chg
    k = 0
    for i in range(Nbat): 
        for t in range(Nt): 
            ub[k] = data['p_bat_max'][i]
            k += 1 
  
    # limtes de p_dch
    for i in range(Nbat): 
        for t in range(Nt): 
            ub[k] = data['p_bat_max'][i]
            k += 1 

    # limtes de soc
    for i in range(Nbat): 
        for t in range(Nt): 
            lb[k] = data['soc_min'][i]
            ub[k] = data['soc_max'][i]
            k += 1 
                        
    return lb, ub

# Exemplo de uso
if __name__ == '__main__':

    from vpp_data import vpp
    from carrega_projecoes import projecoes

    data = vpp()

    Nt = 24
    data["Nt"] = Nt
    Nl = data['Nl']
    Ndl = data['Ndl']
    Npv = data['Npv']
    Nwt = data['Nwt']

    p_l, p_pv, p_wt, p_dl_ref, p_dl_min, p_dl_max, tau_pld, tau_dist, tau_dl = projecoes(Nt, Nl, Ndl, Npv, Nwt)


    lb, ub = vpplimits_PO2(data)

    for i in range(len(lb)):
        if ub[i] < lb[i]:
            print(f'erro {i + 1}')
            break
    print(f'lb é {lb}\n')
    print(f'ub é {ub}')
    

