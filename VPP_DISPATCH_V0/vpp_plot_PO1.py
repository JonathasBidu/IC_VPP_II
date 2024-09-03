import matplotlib.pyplot as plt
import numpy as np

def plot(data):


    Nt = data['Nt']
    Nbm = data['Nbm']
    Ndl = data['Ndl']

    # Biomassa
    p_bm = data['p_bm']
    u_bm = data['u_bm']
    p_bm_max = data['p_bm_max']
    p_bm_min = data['p_bm_min']

    for i in range(Nbm):

        plt.figure(figsize = (10, 5))
        plt.plot(np.ones(Nt) * p_bm_min[i], 'b--')
        plt.plot(np.ones(Nt) * p_bm_max[i], 'b--')
        plt.plot(p_bm[i], 'r')

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