import pandas as pd


path = "C:\\Users\\Jonathas Aguiar\\Desktop\\IC_VPP_II\\VPP_DISPATCH_V0\\Cenários.xlsx"

a = pd.read_excel(path)


for i, j in enumerate(a['p_l']):
    print(f'Cenário {i + 1}')
    print(j)