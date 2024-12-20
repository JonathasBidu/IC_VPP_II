from vpp_create import vpp_create
from carrega_projecoes import projecoes
from vpp_dispatch_PO1 import vpp_dispatch_PO1
from vpp_plot_PO1 import plot

'''
    Descricao do Script:
    Este script realiza a leitura dos parâmetros da vpp, as projeções de
    carga, geração e preço, e os instantes a frente para a programação da 
    vpp, além disso, difine a quantidade de cenários. Ao final desse processo, o script realiza a programação da vpp.
'''

data = vpp_create()

def carrega_cenarios(Ns:int, Nt:int, Nl:int, Ndl:int, Npv:int, Nwt:int)->list:
    scenarios = []
    for n in range(Ns):
        scenario = projecoes(Nt, Nl, Ndl, Npv, Nwt)
        scenarios.append(scenario)
    return scenarios

# N° de instantes desejado
while True:
    Nt = input('N° de horas a frente ou tecle enter para 24 horas: ')
    if Nt == '':
        Nt = 24
        break
    try:
        Nt = int(Nt)
        if Nt > 0:
            Nt = Nt
            break
        else:
            print("Informe um valor numérico válido!")
    except ValueError as v:
        print(f'Informe um valor numérico válido! {v}')
print('')

# Paramêtros da VPP
data['Nt'] = Nt
Nl = int(data['Nl'])
Ndl = int(data['Ndl'])
Npv = int(data['Npv'])
Nwt = int(data['Nwt'])
Nbm = int(data['Nbm'])
Nbat = int(data['Nbat'])



# Carregamento das projeções da VPP
# data['p_l'], data['p_pv'], data['p_wt'], data['p_dl_ref'], data['p_dl_min'], data['p_dl_max'], data['tau_pld'], data['tau_dist'], data['tau_dl'] = projecoes(Nt, Nl, Ndl, Npv, Nwt)

# results, x = vpp_dispatch_PO1(vpp_data)

# vpp_data['p_bm'] = results['p_bm']
# vpp_data['u_bm'] = results['u_bm']
# vpp_data['p_dl'] = results['p_dl']
# vpp_data['u_dl'] = results['u_dl']

# plot(vpp_data)

while True:
    Ns = input("Insira a quantidade de cenários desejados: ")
    if Ns == '':
        Ns = 3
        break
    try:
        Ns = int(Ns)
        if Ns > 0:
            Ns = Ns
            break
        else:
            print('Insira um valor inteiro e positivo!')
    except ValueError as v:
        print(f'Informe um valor numérico válido! {v}')
print('')

data['scenarios'] = carrega_cenarios(Ns, Nt, Nl, Ndl, Npv, Nwt)

print(len(data['scenarios']))


    