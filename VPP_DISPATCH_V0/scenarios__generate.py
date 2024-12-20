from carrega_projecoes import projecoes
from vpp_data import vpp
import pandas as pd
from pathlib import Path

path = Path(__file__).parent

def gera_cenarios(Ns, Nt, Nl, Ndl, Npv, Nwt):

    scenarios = []
    for i in range(Ns):

        p_l, p_pv, p_wt, p_dl_ref, p_dl_min, p_dl_max, tau_pld, tau_dist, tau_dl = projecoes(Nt, Nl, Ndl, Npv, Nwt)
        scenario = {
            'p_l': p_l,
            'p_pv': p_pv,
            'p_wt': p_wt,
            'p_dl_ref': p_dl_ref,
            'p_dl_min': p_dl_min,
            'p_dl_max': p_dl_max,
            'tau_pld': tau_pld,
            'tau_dist': tau_dist,
            'tau_dl': tau_dl
        }

        scenarios.append(scenario)

    return scenarios
                  
if __name__ == '__main__':


    data = vpp()

    Nt = 24  # Número de pontos de dados na série temporal
    Nl = data['Nl']   # Número de cargas
    Ndl = data['Ndl'] # Número de cargas de referência
    Npv = data['Npv']  # Número de sistemas fotovoltaicos
    Nwt = data['Nwt']  # Número de sistemas de geração eólica

    while True:
        Ns = input('Insira a quantidade de cenários desejado: ')
        if Ns == '':
            Ns = 5
            break
        try:
            Ns = int(Ns)
            if Ns > 0:
                Ns = Ns
                break
            else:
                print('Insira um valor inteiro e positivo!')
        except ValueError as v:
            print(f'Informe um valor numérico válido! {v}\n')



    cenario = gera_cenarios(Ns, Nt, Nl, Ndl, Npv, Nwt)

    cenarios_df = pd.DataFrame(cenario)

    cenarios_df.to_excel(path / 'Cenários.xlsx', index = False)

