from decomp_vetor_PO1 import decomp_vetor_x
from decomp_vetor_PO2 import decomp_vetor_y

def teste(x, y, Nscenarios, data):

    Nt = data['Nt']
    Nbm = data['Nbm']
    Ndl = data['Ndl']
    Nbat = data['Nbat']

    p_bm, p_dl, u_bm, u_dl = decomp_vetor_x(x, Nt, Nbm, Ndl)

    p_bm = p_bm.reshape((Nbm, Nt))
    p_dl = p_dl.reshape((Ndl, Nt))
    u_bm = u_bm.reshape((Nbm, Nt))
    u_dl = u_dl.reshape((Ndl, Nt))

    for s in range(Nscenarios):
        p_dl, p_chg, p_dch, soc, u_dl, u_chg, u_dch = decomp_vetor_y(y, Nt, Ndl, Nbat)
        p_dl = p_dl.reshape((Ndl, Nt))
        p_chg = p_chg.reshape((Nbat, Nt))
        p_dch = p_dch.reshape((Nbat, Nt))
        soc = soc.reshape((Nbat, Nt))
        u_dl = u_dl.reshape((Ndl, Nt))
        u_chg = u_chg.reshape((u_dch))