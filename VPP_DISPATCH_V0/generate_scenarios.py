from carrega_projecoes import projecoes
from pathlib import Path
from vpp_data import vpp
import numpy as np
import pickle

# Função para geração de Ns(quantidade de cenários) desejados
def create_scenarios(Ns: int, Nt: int, Nl: int, Ndl: int, Npv: int, Nwt: int) -> list[dict[str, np.ndarray]]:

    scenarios = []
    for s in range(Ns):
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

# Função para salvar os cenários em formato .pkl
def save_scenarios_to_pickle(scenarios: list[dict[str, np.ndarray]], path: Path) -> None:
    with open(path, 'wb') as file:
        pickle.dump(scenarios, file)

# Função para carregar os cenários de um arquivo .pkl
def import_scenarios_from_pickle(path: Path) -> list[dict[str, np.ndarray]]:

    with open(path, 'rb') as file:
        scenarios = pickle.load(file)
    return scenarios

# Teste de uso   
if __name__ == '__main__':

    # Obtendo os parâmetros da VPP
    data = vpp()
    Nt = 24  # Número de pontos de dados na série temporal
    Nl = data['Nl']   # Número de cargas
    Ndl = data['Ndl'] # Número de cargas de referência
    Npv = data['Npv']  # Número de sistemas fotovoltaicos
    Nwt = data['Nwt']  # Número de sistemas de geração eólica

    # Definindo uma quantidade de cenários
    while True:
        Ns = input('Insira a quantidade de cenários desejado: ')
        if Ns == '':
            Ns = 11
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

    # # Gerando uma quantidade de Ns cenários
    # scenarios = create_scenarios(Ns, Nt, Nl, Ndl, Npv, Nwt)

    # # Salvando os Ns cenários em um arquivo .pkl
    # path = Path(__file__).parent / 'Cenários.pkl'
    # save_scenarios_to_pickle(scenarios, path)

    # Carregando os cenários do arquivo .pkl  
    path_cenarios = Path(__file__).parent / 'Cenários.pkl'
    cenarios = import_scenarios_from_pickle(path_cenarios)

    print(type(cenarios))
    # print(len(cenarios))

    print(cenarios[0]['p_l'])

    p_ls = []
    tau_dist = []
    p_pvs = []

    for cenario in cenarios:
        p_ls.append(cenario['p_l'])
        tau_dist.append(cenario['tau_dist'])
        p_pvs.append(cenario['p_pv'])

  
    Cl = 0
    for cenario in range(Ns):
        for i in range(Nl):
            for t in range(Nt):
                Cl += p_ls[cenario][i, t] * tau_dist[cenario][t]

    print(f'Cl = {Cl:.2f}')
    print(type(Cl))
