import numpy as np
"""
    Esta função decompõe o vetor de variáveis de controle em suas componentes constituintes.

    Parâmetros:
        - x: Vetor de entrada de variáveis de controle que possui a forma x = [xr, xi]
            - xr: vetor de variáveis reais, que por sua vez tem forma xr = [p_bm, p_dl, p_chg, p_dch, soc]
                Em cada subvetor, as potências são arranjadas por instante e por usina. Por exemplo, se Nt = 3 e Nbm = 2 entao: 
                p_bm = [p_bm_1_1, p_bm_1_2, p_bm_1_3, p_bm_2_1, p_bm_2_2, p_bm_2_3] onde p_bm_i_j representa a potencia da UTE Biomassa i no instante(hora) j.

            - xi: vetor de variáveis inteiras, que possuí a forma x = [u_bm, u_dl, u_chg, u_dch]
                Em cada subvetor, as potências são arranjadas por instante e por usina. Por exemplo, se Nt = 3 e Nbm = 2 entao: 
                u_bm = [u_bm_1_1, u_bm_1_2, u_bm_1_3, u_bm_2_1, u_bm_2_2, u_bm_2_3] onde u_bm_i_j representa o status da UTE Biomassa i no instante(hora) j.

        - Nt: Número de instantes de tempo
        - Ndl: Número de cargas despacháveis
        - Nbat: Número de baterias

    Retorna:
        - p_dl: Vetor de potência da carga despachável, forma (Ndl * Nt, 1)
        - p_chg: Vetor de potência de carga da bateria, forma (Nbat * Nt, 1)
        - p_dch: Vetor de potência de descarga da bateria, forma (Nbat * Nt, 1)
        - soc: Vetor de estado de carga da bateria, forma (Nbat * Nt, 1)
        - u_dl: Vetor de status da carga despachável, forma (Ndl * Nt, 1)
        - u_chg: Vetor de status de carga da bateria, forma (Nbat * Nt, 1)
        - u_dch: Vetor de status de descarga da bateria, forma (Nbat * Nt, 1)
"""

def decomp_vetor_y(y, Nt: int, Ndl: int, Nbat: int)-> tuple:

    # Calculando as variáveis reais e inteira
    Nr = (Nbat * Nt) + (Nbat * Nt) + (Nbat * Nt)
    Ni = (Nbat * Nt) + (Nbat * Nt)

    inicio = 0
    fim = Nr
    yr = np.array(y[inicio: fim])

    # obtenção de p_chg
    inicio = 0
    fim = (Nbat * Nt)
    p_chg = yr[inicio: fim]

    # obtenção de p_dch
    inicio = fim
    fim = fim + (Nbat * Nt)
    p_dch = yr[inicio: fim]

    # obtenção de soc
    inicio = fim
    fim = fim + (Nbat * Nt)
    soc = yr[inicio: fim]

    inicio = 0
    fim = Ni
    yi = np.array(y[inicio: fim])

    # obtenção de u_chg
    inicio = 0
    fim = (Nbat * Nt)
    u_chg = yi[inicio:fim]

    # obtenção de u_dch
    inicio = fim
    fim = fim + (Nbat * Nt)
    u_dch = yi[inicio: fim]

    u_chg = np.float64(u_chg > 0.5)
    u_dch = np.float64(u_dch > 0.5)

    return p_chg, p_dch, soc, u_chg, u_dch


# Exemplos de uso
if __name__ == '__main__':
        
    Nt = 24 # Número de instantes de tempo a frente
    Nbm = 2 # Número de usinas de biomassa
    Ndl = 3 # Número de cargas despacháveis
    Nbat = 4 # Número de bateria
    Nr = (Nt * Ndl) + (Nt * Nbat) + (Nbat * Nt) + (Nbat * Nt)
    Ni = (Nt * Ndl) + (Nbat * Nt) + (Nbat * Nt)

    y = np.random.rand(Nr + Ni)
    p_chg, p_dch, soc, u_chg, u_dch = decomp_vetor_y(y, Nt, Ndl, Nbat)

    # xr = np.concatenate((p_dl, p_chg, p_dch, soc, u_dl, u_chg, u_dch))
    # print(p_dl, f' o tipo é p_dl{type(p_dl)} e o  seu shape é {p_dl.shape}','\n')
    print(p_chg, f' o tipo é p_chg{type(p_chg)} e o  seu shape é {p_chg.shape}','\n')
    print(p_dch, f' o tipo é p_dch{type(p_dch)} e o  seu shape é {p_dch.shape}','\n')
    print(soc, f' o tipo é soc{type(soc)} e o  seu shape é {soc.shape}','\n')
    # print(u_dl, f' o tipo é u_dl{type(u_dl)} e o  seu shape é {u_dl.shape}','\n')
    print(u_chg, f' o tipo é u_chg{type(u_chg)} e o  seu shape é {u_chg.shape}','\n')
    print(u_dch, f' o tipo é u_dch{type(u_dch)} e o  seu shape é {u_dch.shape}','\n')
