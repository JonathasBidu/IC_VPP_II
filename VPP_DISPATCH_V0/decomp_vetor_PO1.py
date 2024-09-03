import numpy as np

'''
    Esta função decompõe o vetor x de variáveis de controle em suas componentes constituintes.

    - Parâmetros:
        - vetor x:
            - Atributos -> p_bm, u_bm e p_l
                - p_bm : potência das usinas de biomassa de dimensão (Nbm, Nt), onde, Nbm corresponde ao número de biomassa e Nt corresponde ao instante de tempo à frente.
                - u_bm : estado(ligado/desligado) das usinas de biomassa de dimensão (Nbm, Nt).
                - p_l : potência das cargas despachaveis de dimensão (Nl, Nt), onde, Nl corresponde a quantidade de cargas despachaveis.
            - Nt : instantes de tempo à frente.
            - Nbm : quantidade de usinas de biomassa.
            - Nl : quantidade de cargas despachaveis.

    - Retorno:
        - Tupla: (p_bm, p_dl, u_bm, u_dl)
            - p_bm : potência das usinas de biomassa.
            - p_l : potência das cargas despachaveis.
            - u_bm : estado(ligado/desligado) das usianas de biomassa.
            - u_dl : estado(ligado/desligado) das cargas despachaveis.
'''

def decomp_vetor_x(x, Nt, Nbm, Ndl):

    # separacao entre xr e xi
    Nr = (Nt * Nbm) + (Nt * Ndl)
    Ni = (Nt * Nbm) + (Nt * Ndl)

    # criação do vetor de varáveis reais xr
    inicio = 0
    fim = Nr
    xr = np.array(x[inicio: fim])

    # obtenção de p_bm (potência da biomassa)
    inicio = 0
    fim = (Nbm * Nt)
    p_bm = xr[inicio: fim]

    # obtenção de p_dl (potência da carga despachavel)
    inicio = fim
    fim = fim + (Nt * Ndl)
    p_dl = xr[inicio: fim]

    # criação do vetor de varáveis reais xi
    inicio = 0
    fim = fim + Ni
    xi = np.array(x[inicio: fim])

    # obtenção de u_bm (estado da usina de biomassa(ligado/desligado))
    inicio =  0
    fim = (Nbm * Nt)
    u_bm = xi[inicio: fim]

    # obtenção de u_dl (estado da carga despachavel(ligado/desligado))
    inicio = fim
    fim = fim + (Nt * Ndl)
    u_dl = xi[inicio: fim]

    # lógica para caso o número seja maior 0.5 ela receba o sinal alto ou caso ao contrário receba o sinal baixo
    u_bm = np.float64(u_bm > 0.5)
    u_dl = np.float64(u_dl > 0.5)

    return p_bm, p_dl, u_bm, u_dl

# # Array de teste:
# from vpp_data import vpp

# data = vpp()

# Nt = 24 # Número de instantes de tempo a frente
# data['Nt'] = Nt
# Nbm = data['Nbm']
# Ndl = data['Ndl']

# Nr = Nt * Nbm + Nt * Ndl
# Ni = Nt * Nbm + Nt * Ndl

# x = np.random.rand(Nr + Ni)

# p_bm, p_dl, u_bm, u_dl = decomp_vetor_x(x, Nt, Nbm, Ndl)

# print(f' o tipo é p_bm {type(p_bm)} e o  seu shape é {p_bm.shape}','\n', p_bm, '\n')
# print(f' o tipo é u_bm {type(u_bm)} e o  seu shape é {u_bm.shape}','\n', u_bm, '\n')
# print(f' o tipo é p_dl {type(p_dl)} e o  seu shape é {p_dl.shape}','\n', p_dl, '\n')
# print(f' o tipo é u_bm {type(u_dl)} e o  seu shape é {u_dl.shape}','\n', u_dl, '\n')