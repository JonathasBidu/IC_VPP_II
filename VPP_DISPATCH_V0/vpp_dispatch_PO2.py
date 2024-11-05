import numpy as np
from func_aux_2 import func
from constraints_PO2 import const_PO2
from get_limits_PO2 import vpplimits_PO2
from decomp_vetor_PO2 import decomp_vetor_y
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize

from pymoo.config import Config
Config.warnings['not_compiled'] = False

""" 
    Descrição da função:
    Esta função realiza o despacho de uma VPP utilizando um algoritmo genético com base em cenários de geração FV, Eólica e de Consumo, a VPP busca definir a melhor composição de geração biomassa, armazenamento e cargas despacháveis que maximiza o retorno financeiro.

    Parâmetros:
        - vpp_data: estrutura de dicionário contendo os dados de geradores, cargas e armazenadores da VPP.

    Retorna:
        - Lucro: Lucro obtido no despacho da usina
        - p_exp: vetor de potência exportadas, dimensão (Nt, 1)
        - p_imp: vetor de potência importada, dimensão (Nt, 1)
        - p_bm: vetor de potência das UTEs biomassa, dimensão ((Nbm * Nt), 1)
        - p_dl: vetor de potência das cargas despacháveis, dimensão ((Ndl * Nt), 1)
        - p_chg: vetor de potência de carga das baterias, dimensão ((Nbat * Nt), 1)
        - p_dch: vetor de pot. de descarga das bateria, dimensão ((Nbat * Nt), 1)
        - soc: vetor de status de carga das baterias, dimensão ((Nbat * Nt), 1)
        - u_exp: vetor de status de potência exportadas, dimensão (Nt, 1)
        - u_imp: vetor de status de potência importada, dimensão (Nt, 1)
        - u_bm: vetor de status das UTEs biomassa, dimensão ((Nbm * Nt), 1)
        - u_dl: vetor de status das cargas despacháveis, dimensão ((Ndl * Nt), 1)
        - u_chg: vetor de status de carga das baterias, dimensão ((Nbat * Nt), 1)
        - u_dch: vetor de status de descarga das bateria, dimensão ((Nbat * Nt), 1)
"""

# Otimização utilizando Ga(Genetic algorithm)
def vpp_dispatch_PO2(vpp_data):

    Nt = vpp_data['Nt']
    Ndl = vpp_data['Ndl']
    Nbat = vpp_data['Nbat']
       
    # Definição das variáveis inteiras e do número de variáveis
    Nr = (Nbat * Nt) + (Nbat * Nt) + (Nbat * Nt) 
    Ni = (Nbat * Nt) + (Nbat * Nt) 
    
    # Número de variáveis
    nvars = Nr + Ni
   
    # -> Obtendo a quantidade de inequações
    # Quantidade de restrições das baterias
    Nbatc = ((Nt - 1) * Nbat) + (Nt*Nbat) + (Nt*Nbat) + (Nt*Nbat) + ((Nt - 1) * Nbat)   
     # Quantidade de restrições das cargas despachaveis
    # Quantidade total de restrições                                                   
    n_constr_ieq = Nbatc

    # obtendo os limites superiores e inferiores
    lb, ub = vpplimits_PO2(vpp_data)

    class MyProblem(ElementwiseProblem):

        def __init__(self, vpp_data, **kwargs):
            super().__init__(vpp_data, **kwargs)
            self.data = vpp_data

        def _evaluate(self, y, out, *args, **kwargs):

            out['F'] = np.array([ - func(y, self.data)])
            out['G'] = const_PO2(y, self.data)
            
    problem = MyProblem(vpp_data,
                        n_var = nvars,
                        n_obj = 1,
                        n_ieq_constr = n_constr_ieq,
                        xl = lb,
                        xu = ub
                        )
    
    algorithm = GA(pop_size = 50)
    termination = (('n_gen', 50))  

    # MODELO FEITO COM PENALIDADES NAS RESTRIÇÕES
    from pymoo.constraints.as_penalty import ConstraintsAsPenalty
    from pymoo.core.evaluator import Evaluator
    from pymoo.core.individual import Individual

    res = minimize(ConstraintsAsPenalty(problem, penalty = 100.0), algorithm, termination, seed = 1, verbose = False)
    res = Evaluator().eval(problem, Individual(X = res.X))

    # MODELO SEM PENALIDADES DE RESTRIÇÃO
    # res = minimize(problem,
    #                algorithm,
    #                termination,
    #                seed = 1,
    #                verbose = True
    #                )
    
    # GERAÇÃO DE RESULTADOS
    results = {}
    results['Lucro'] = - res.F[0]
    y = res.X

    results['VL'] = res.CV[0]

    # print(f'\nNessa simulação o lucro foi de {- res.F[0]:.2f} R$')
    # print(f'\nO total de violações foi {res.CV[0]:.2f}\n')
    
    # Decompõe o vetor de variáveis de decisão em matrizes
    p_chg, p_dch, soc, u_chg, u_dch = decomp_vetor_y(y, Nt, Nbat) 

    # Reshape dos vetores em matrizes
    results['p_chg'] = p_chg.reshape((Nbat, Nt))
    results['p_dch'] = p_dch.reshape((Nbat, Nt))
    results['soc'] = soc.reshape((Nbat, Nt))
    results['u_chg'] = u_chg.reshape((Nbat, Nt))
    results['u_dch'] = u_dch.reshape((Nbat, Nt))

    return results, y