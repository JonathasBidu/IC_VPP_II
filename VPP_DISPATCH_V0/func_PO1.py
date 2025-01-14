from decomp_vetor_PO1 import decomp_vetor_x
from decomp_vetor_PO2 import decomp_vetor_y
from get_limits_PO2 import vpplimits_PO2
from constraints_PO2  import const_PO2
from func_PO2 import func_PO2
from generate_scenarios import import_scenarios_from_pickle
import numpy as np

'''
    Esta função é a função do problema de primeiro estágio.

    - Parâmetros:
        - vetor x:
            - Atributos -> p_bm, u_bm e p_l
                - p_bm : potência das usinas de biomassa de dimensão (Nbm, Nt), onde, Nbm corresponde ao número de biomassa e Nt corresponde ao instante de tempo à frente.
                - u_bm : estado(ligado/desligado) das usinas de biomassa de dimensão (Nbm, Nt).
                - p_l : potência das cargas despachaveis de dimensão (Nl, Nt), onde, Nl corresponde a quantidade de cargas despachaveis.
        - data : dicionário contendo parâmetros iniciais da vpp.
            - Atributos:
                - Nbm : quantidade de usinas de biomassa.
                - Ndl : quantidade de cargas não despachaveis.
                - Nl : quantidade de cargas despachaveis.
                - Npv : quantidade de usinas fotovoltaicas.
                - Nwt : quantidade de usinas eólicas.
                - Nbat : quantidade de armazenadores.
                - p_bm_min : potência mínima das usinas de biomassa.
                - p_bm_max : potência máxima das usinas de biomassa.
                - p_bm_rup : potência de subida das usina de biomassa.
                - p_bm_rdown : potência de descida das usinas de biomassa.
                - kappa_bm : preço de custo operciaonal das usinas de biomassa.
                - kappa_bm_start : preço de custo de partida das usinas de biomassa.
                - kappa_pv : preço de custo operacional das usinas fotovoltaicas.
                - kappa_wt : preço de custo operacional das usinas eólicas.
                - kappa_bat : preço de custo opercional dos armazenadores.
                - soc_min : balanço mínimo dos armazenadores.
                - soc_max : balanço máximo dos armazenadores.
                - eta_chg : rendimento da carga da bateria.
                - eta_dch : rendimento da descarga da bateria.
                - p_bat_max : potência máxima suportada pelos armazenadores.

    - Retorna: 
        - fval:
            - Atributos:
                - Cbm : vetor contendo os custos opercionais das usinas de biomassa.
                - Cdl : vetor contendo os custos operacionais do controle de carga.

'''

def vpp_func_PO1(x: np.ndarray, data: dict, Ns: int)-> float:

    Nt = data['Nt']
    Nbm = data['Nbm']  
    Ndl = data['Ndl']  
    Nbat = data['Nbat']  
    kappa_bm = data['kappa_bm']
    kappa_bm_start = data['kappa_bm_start']
    tau_dl = data['tau_dl']

    #  Separação das variaveis no vetor solução
    p_bm, p_dl, u_bm, u_dl = decomp_vetor_x(x, Nt, Nbm, Ndl)
    
    # Reshape vetores em matrizes
    p_bm = p_bm.reshape((Nbm, Nt))
    u_bm = u_bm.reshape((Nbm, Nt))
    p_dl = p_dl.reshape((Ndl, Nt))
    u_dl = u_dl.reshape((Ndl, Nt))

    # Custos de geração biomassa (custo linear)
    Cbm = 0
    for t in range(Nt):
        for i in range(Nbm):
            Cbm += p_bm[i, t] * u_bm[i, t] * kappa_bm[i]
    
    #  custo de partida
    for t in range(1, Nt):
        for i in range(Nbm):
            Cbm += (u_bm[i, t] - u_bm[i, t - 1]) * kappa_bm_start[i]

    # Custo de controle de carga despachada
    Cdl = 0
    for t in range(Nt):
        for i in range(Ndl):
            Cdl += p_dl[i, t] * u_dl[i, t] * tau_dl[t]
    
    # Solução do problema de segundo estágio (PO2) para diferentes cenários
    Eq = 0

    # Obtendo o caminho do arquivo que contém os cenários gerados
    path_to_scenarios = 'C:\\Users\\Jonathas Aguiar\\Desktop\\IC_VPP_II\\VPP_DISPATCH_V0\\Cenários.pkl'
    scenarios = import_scenarios_from_pickle(path_to_scenarios)

    for s in range(Ns):

        print(f'\nOtimização do 2° estágio para o cenário {s + 1}')
        # Atualizar os cenários
        # p_l, p_pv, p_wt, p_dl_ref, p_dl_min, p_dl_max, tau_pld, tau_dist, tau_dl || variáveis retornadas pela função carrega projeções

        # Variáveis usadas pela func_PO2
        # p_pv = data['p_pv']
        # p_wt = data['p_wt']
        # p_l = data['p_l']
        # tau_pld = data['tau_pld']
        # tau_dist = data['tau_dist']
        # tau_dl = data['tau_dl']   

        # Atualização das projeções
        data['p_pv'] = scenarios[s]['p_pv']
        data['p_wt'] = scenarios[s]['p_wt']
        data['p_l'] = scenarios[s]['p_l']
        data['tau_pld'] = scenarios[s]['tau_pld']
        data['tau_dist'] = scenarios[s]['tau_dist']
        data['tau_dl'] = scenarios[s]['tau_dl']


        # Definindo a quantidade de variáves reais e inteiras
        Nr = (Nbat * Nt) + (Nbat * Nt) + (Nbat * Nt)
        Ni = (Nbat * Nt) + (Nbat * Nt) 
        Nvars_PO2 = Nr + Ni

        # Definindo a quantidade de restrições do segundo estágio 
        n_const_ieq_PO2 = ((Nt - 1) * Nbat) + ((Nt - 1) * Nbat) + (Nt * Nbat) + (Nt* Nbat) + (Nt * Nbat)

        # Obtendo os limites inferiores e superiores do PO2
        lb_PO2, ub_PO2 = vpplimits_PO2(data)

        from pymoo.core.problem import ElementwiseProblem
        from pymoo.algorithms.soo.nonconvex.ga import GA
        from pymoo.optimize import minimize

        class MyProblem(ElementwiseProblem):

            def __init__(self, data, **kwargs):
                super().__init__(data, **kwargs)
                self.data = data

            def _evaluate(self, y, out, *args, **kwargs):
                
                out['F'] = np.array([- func_PO2(y, self.data)])
                out['G'] = const_PO2(y, self.data)

        # Insatanciando a classe MyProblem
        problem_PO2 = MyProblem(data,
                                n_var = Nvars_PO2,
                                n_obj = 1,
                                n_ieq_constr =  n_const_ieq_PO2,
                                xl = lb_PO2,
                                xu = ub_PO2)
        
        # Definido o algoritmo
        algorithm_PO2 = GA(pop_size = 10)
        termination_PO2 = (('n_gen', 10))  

        from pymoo.constraints.as_penalty import ConstraintsAsPenalty
        from pymoo.core.evaluator import Evaluator
        from pymoo.core.individual import Individual

        res_PO2 = minimize(ConstraintsAsPenalty(problem_PO2, penalty = 100.0), algorithm_PO2, termination_PO2, seed = 1, verbose = True)
        res_PO2 = Evaluator().eval(problem_PO2, Individual(X = res_PO2.X))

        # res_PO2 = minimize(problem = problem_PO2,
        #                    algorithm = algorithm_PO2,
        #                    termination = termination_PO2,
        #                    seed = 1,
        #                    verbose = True)
        

        if res_PO2.CV[0] == 0.0:
            data = {}
            data['lucro'] = res_PO2.F[0]

            # Obtendo os despachos otimizados do segundo estágio
            y = res_PO2.X
            p_chg, p_dch, soc, u_chg, u_dch = decomp_vetor_y(y, Nt, Nbat)
            data['p_chg'] = p_chg.reshape((Nbat, Nt))
            data['p_dch'] = p_dch.reshape((Nbat, Nt))
            data['soc'] = soc.reshape((Nbat, Nt))
            data['u_chg'] = u_chg.reshape((Nbat, Nt))
            data['u_dch'] = u_dch.reshape((Nbat, Nt))
            q = res_PO2.F[0]

            break

    
        data['lucro'] = res_PO2.F[0]
        y = res_PO2.X

        p_chg, p_dch, soc, u_chg, u_dch = decomp_vetor_y(y, Nt, Nbat)
        data['p_chg'] = p_chg.reshape((Nbat, Nt))
        data['p_dch'] = p_dch.reshape((Nbat, Nt))
        data['soc'] = soc.reshape((Nbat, Nt))
        data['u_chg'] = u_chg.reshape((Nbat, Nt))
        data['u_dch'] = u_dch.reshape((Nbat, Nt))

        q = res_PO2.F[0]
        Eq += q
    Eq = np.float64(Eq / Ns)

    # Despesa total
    fval = Cbm + Cdl + Eq
    
    return fval, res_PO2

# Exemplo de uso:
if __name__ == '__main__':

    from vpp_data import vpp
    from carrega_projecoes import projecoes
    from pymoo.config import Config
    Config.warnings['not_compiled'] = False
    

    data = vpp()

    Nt = 24
    data['Nt'] = Nt
    Nbm = data['Nbm']
    Nl = data['Nl']
    Ndl = data['Ndl']
    Npv = data['Npv']
    Nwt = data['Nwt']

    
    p_l, p_pv, p_wt, p_dl_ref, p_dl_min, p_dl_max, tau_pld, tau_dist, tau_dl = projecoes(Nt, Nl, Ndl, Npv, Nwt)

    data['tau_dl'] = tau_dl
    data['p_pv'] = p_pv
    data['p_wt'] = p_wt
    data['p_l'] = p_l
    data['tau_dist'] = tau_dist
    data['tau_dl'] = tau_dl
    data['tau_pld'] = tau_pld
    data['p_dl_ref'] = p_dl_ref
    data['p_dl_min'] = p_dl_min
    data['p_dl_max'] = p_dl_max

    Nr = Nt * Nbm + Nt * Ndl
    Ni = Nt * Nbm + Nt * Ndl
    x = np.random.rand(Nr + Ni)

    Nscenarios = int(input('qtd de cenários: '))

    func, res = vpp_func_PO1(x, data, Nscenarios)

    print('\nVizualizão da função objetivo do problema de primeiro estágio')
    print(func)
    print('')
    print(res.F)  # contém o valor da função objetivo para a solução encontrada, que é o valor otimizado da função.
    print(res.CV) # contém as violações das restrições. Se for 0, a solução é viável. Se for maior que 0, há violação.
    print(res.X)  # contém os valores das variáveis de decisão (parâmetros) para a solução encontrada.
    print(res.G)  # contém os valores das restrições (normalmente a função das restrições) para a solução encontrada.

