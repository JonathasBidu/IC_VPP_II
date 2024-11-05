from vpp_create import vpp_create
from carrega_projecoes import projecoes
from vpp_dispatch_PO1 import vpp_dispatch_PO1
from vpp_dispatch_PO2 import vpp_dispatch_PO2
from vpp_plot_test import plot

''' Esse script...'''

vpp_data = vpp_create()

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

# Qtd de cenários
while True:
    Nscenario = input('Qtd de cenários ou tecle enter para 3: ')
    if Nscenario == '':
        Nscenario = 3
        break
    try:
        Nscenario = int(Nscenario)
        if Nscenario > 0:
            Nscenario = Nscenario
            break
        else:
            print("Informe um valor numérico válido!")
    except ValueError as v:
        print(f'Informe um valor numérico válido! {v}')
print('')

# Paramêtros da VPP
vpp_data['Nt'] = Nt
Nl = int(vpp_data['Nl'])
Ndl = int(vpp_data['Ndl'])
Npv = int(vpp_data['Npv'])
Nwt = int(vpp_data['Nwt'])
Nbm = int(vpp_data['Nbm'])
Nbat = int(vpp_data['Nbat'])

# Carregamento das projeções da VPP
vpp_data['p_l'], vpp_data['p_pv'], vpp_data['p_wt'], vpp_data['p_dl_ref'], vpp_data['p_dl_min'], vpp_data['p_dl_max'], vpp_data['tau_pld'], vpp_data['tau_dist'], vpp_data['tau_dl'] = projecoes(Nt, Nl, Ndl, Npv, Nwt)

# otimização do primeiro estágio
results_PO1, x = vpp_dispatch_PO1(vpp_data)

# Variáveis do primeiro estágio
vpp_data['p_bm'] = results_PO1['p_bm']
vpp_data['u_bm'] = results_PO1['u_bm']
vpp_data['p_dl'] = results_PO1['p_dl']
vpp_data['u_dl'] = results_PO1['u_dl']

for s in range(Nscenario):


    vpp_data['p_l'], vpp_data['p_pv'], vpp_data['p_wt'], vpp_data['p_dl_ref'], vpp_data['p_dl_min'], vpp_data['p_dl_max'], vpp_data['tau_pld'], vpp_data['tau_dist'], vpp_data['tau_dl'] = projecoes(Nt, Nl, Ndl, Npv, Nwt)


    results_PO2, y = vpp_dispatch_PO2(vpp_data)

    vpp_data['p_chg'] = results_PO2['p_chg']
    vpp_data['p_dch'] = results_PO2['p_dch']
    vpp_data['u_chg'] = results_PO2['u_chg']
    vpp_data['u_dch'] = results_PO2['u_dch']
    vpp_data['soc'] = results_PO2['soc']

    print(f's == {s+1}')

plot(vpp_data)
print(f'Para essa simulação o lucro foi de {results_PO2['Lucro']:.2f}\n')
print(f"O total de violações foi de {results_PO2['VL']:.2f}")