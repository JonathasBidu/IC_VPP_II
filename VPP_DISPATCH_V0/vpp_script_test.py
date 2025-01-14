from vpp_create import vpp_create
from carrega_projecoes import projecoes
from vpp_dispatch_PO1 import vpp_dispatch_PO1

''' Esse script...'''

data = vpp_create()

# Intervalo da simulação
while True:
    Nt = input('Insira o intervalo da simulação ou tecle enter para 24 horas: ')
    if Nt == '':
        Nt = 24
        break
    try:
        Nt = int(Nt)
        if Nt > 0:
            Nt = Nt
            break
        else:
            print("Informe um valor inteiro e positivo!")
    except ValueError as v:
        print(f'Informe um valor numérico válido! {v}')
print('')

# Qtd de cenários
while True:
    Ns = input('Insira a quantidade de cenários desejado ou tecle enter para 11 cenários: ')
    if Ns == '':
        Ns = 11
        break
    try:
        Ns = int(Ns)
        if Ns > 0:
            Ns = Ns
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
data['p_l'], data['p_pv'], data['p_wt'], data['p_dl_ref'], data['p_dl_min'], data['p_dl_max'], data['tau_pld'], data['tau_dist'], data['tau_dl'] = projecoes(Nt, Nl, Ndl, Npv, Nwt)

# otimização do primeiro estágio
results_PO1, x = vpp_dispatch_PO1(Ns, data)

print(data['p_chg'])