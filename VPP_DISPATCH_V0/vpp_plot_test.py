import numpy as np
import matplotlib.pyplot as plt

def plot(data):

    # Paramêtros da VPP
    Nt = data['Nt']
    Nl = int(data['Nl'])
    Ndl = int(data['Ndl'])
    Npv = int(data['Npv'])
    Nwt = int(data['Nwt'])
    Nbm = int(data['Nbm'])
    Nbat = int(data['Nbat'])

    t = np.arange(1, Nt + 1)

    # Biomassa
    p_bm = data['p_bm']
    u_bm = data['u_bm']
    p_bm_max = data['p_bm_max']
    p_bm_min = data['p_bm_min']

    for i in range(Nbm):

        plt.figure(figsize = (10, 4))
        plt.plot(np.ones(Nt) * p_bm_max[i],'r--')
        plt.plot(np.ones(Nt) * p_bm_min[i],'r--')
        plt.plot(p_bm[i],'b')

        title_name = f'Usina de Biomassa {i + 1}'
        plt.title(title_name)
        plt.xlabel('Hora')
        plt.ylabel('Potência em MW')
        plt.legend(['min', 'max', 'p'])
        plt.show()

        plt.figure(figsize = (10, 4))
        plt.step(u_bm[i], 'r')
        title_name = f'Estado da Biomassa {i + 1}'
        plt.title(title_name)
        plt.show()

    p_dl_ref = data['p_dl_ref']
    p_dl_min = data['p_dl_min']
    p_dl_max = data['p_dl_max']
    p_dl = data['p_dl']

    for i in range(Ndl):

        plt.figure(figsize = (10, 4))
        plt.plot(p_dl_ref[i, :], 'r')
        plt.plot(p_dl_max[i, :], 'b--')
        plt.plot(p_dl_min[i, :], 'b--')
        plt.plot(p_dl[i, :], 'k')

        title_name = f'Cargas despachaveis {i + 1}'
        plt.title(title_name)
        plt.xlabel('Hora')
        plt.ylabel('Potência em MW')
        plt.legend(['ref', 'min', 'max', 'desp'])
        plt.show()

    p_l = data['p_l']

    for i in range(Nl):

        plt.figure(figsize = (12, 5))
        plt.title(f'Carga NÃO despachável{i + 1}')
        plt.plot(p_l[i, :], 'r')
        plt.xlabel('hora')
        plt.ylabel('Potência em MW')
        plt.show()

    # Plot dos Armazenadores
    Nbat = data['Nbat']
    p_chg = data['p_chg']
    p_dch = data['p_dch']
    u_dch = data['u_dch']
    u_chg = data['u_chg']
    soc = data['soc']
    soc_min = data['soc_min']
    soc_max = data['soc_max']
    p_bat_max = data['p_bat_max']

    for i in range(Nbat):

        plt.figure(figsize = (12, 5))
        plt.title(f' Carga Bateria {i + 1}')
        plt.plot(t, p_bat_max[i] * np.ones(Nt), 'b--')
        plt.step(t, p_chg[i, :] * u_chg[i, :], 'r')
        plt.xlabel('hora')
        plt.ylabel('carga')
        plt.show()

        plt.figure(figsize = (12, 5))
        plt.title(f' Descarga Bateria {i + 1}')
        plt.plot(t, p_bat_max[i] * np.ones(Nt), 'b--')
        plt.step(t, p_dch[i, :] * u_dch[i, :], 'r')
        plt.xlabel('hora')
        plt.ylabel('carga')
        plt.show()

        plt.figure(figsize = (12, 5))
        plt.title(f' Soc Bateria {i + 1}')
        plt.plot(t, soc_min[i] * np.ones(Nt) , 'b--')
        plt.plot(t, soc_max[i] * np.ones(Nt) , 'b--')
        plt.step(t, soc[i,:], 'r')
        plt.xlabel('hora')
        plt.ylabel('carga')
        plt.show()

    p_pv = data['p_pv']

    for i in range(Npv):

        plt.figure(figsize = (12, 5))
        plt.title(f'Usina Solar {i + 1}')
        plt.plot(p_pv[i])
        plt.xlabel('hora')
        plt.ylabel('Potência em MW')
        plt.show()

    p_wt = data['p_wt']

    for i in range(Nwt):
        
        plt.figure(figsize = (12, 5))
        plt.title(f'Usina Eólica {i + 1}')
        plt.plot(p_wt[i])
        plt.xlabel('hora')
        plt.ylabel('Potência em MW')
        plt.show()