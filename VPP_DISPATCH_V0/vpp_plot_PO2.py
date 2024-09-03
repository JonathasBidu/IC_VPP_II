import matplotlib.pyplot as plt
import numpy as np

def plot(data):

    Nt = data['Nt']
    t = np.arange(1, Nt + 1)

    Ndl = data['Ndl']
    p_dl_ref = data['p_dl_ref']
    p_dl_min = data['p_dl_min']
    p_dl_max = data['p_dl_max']

    p_dl = data['p_dl']

    for i in range(Ndl):

        plt.figure(figsize = (12, 5))
        plt.title(f'Carga {i + 1}')
        plt.plot(p_dl_max[i, :])
        plt.plot(p_dl_min[i, :])
        plt.plot(p_dl_ref[i, :])
        plt.plot(p_dl[i, :])
        plt.xlabel('hora')
        plt.ylabel('Potência em MW')
        plt.legend(['ref', 'min', 'max', 'desp'])
        plt.show()

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