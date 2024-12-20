from vpp_create import vpp_create
from carrega_projecoes import projecoes
from vpp_dispatch_PO2 import vpp_dispatch_PO2
from vpp_plot_PO2 import plot

'''
    Descricao do Script:
    Este script realiza a leitura dos parâmetros da vpp, as projeções de
    carga, geração e preço, e os instantes a frente para a programação da 
    vpp, além disso, difine a quantidade de cenários. Ao final desse processo, o script realiza a programação da vpp.
'''

vpp_data = vpp_create()

# N° de instantes desejado
while True:
    Nt = input('N° de horas a frente ou tecle enter para 24 horas: ')
    print('')
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

results, x = vpp_dispatch_PO2(vpp_data)

vpp_data['p_chg'] = results['p_chg']
vpp_data['p_dch'] = results['p_dch']
vpp_data['soc'] = results['soc']
vpp_data['u_chg'] = results['u_chg']
vpp_data['u_dch'] = results['u_dch']

plot(vpp_data)