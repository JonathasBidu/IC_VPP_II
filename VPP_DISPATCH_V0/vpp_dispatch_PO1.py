import numpy as np
from func_PO1 import vpp_func_PO1
from constraints_PO1 import const_PO1
from get_limits_PO1 import vpplimits_PO1
from decomp_vetor_PO1 import decomp_vetor_x
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize

from pymoo.config import Config
Config.warnings['not_compiled'] = False

# Otimização utilizando Ga(Genetic algorithm)
def vpp_dispatch_PO1(Ns, vpp_data):

    # Obtendo os parâmetros inicias da vpp.
    Nt = vpp_data['Nt']
    Nbm = vpp_data['Nbm']
    Ndl = vpp_data['Ndl']

    # Definição das variáveis inteiras e do número de variáveis.
    Nr = (Nbm * Nt) + (Nt * Ndl)
    Ni = (Nbm * Nt) + (Nt * Ndl)

    # Número de variáveis.
    nvars = Nr + Ni

    n_constr_ieq = (Nt * Nbm) + (Nt * Nbm) + ((Nt - 1) * Nbm) + ((Nt - 1) * Nbm) + (Nt * Ndl) + (Nt * Ndl) 
    lb, ub = vpplimits_PO1(vpp_data)

    class MyProblem(ElementwiseProblem):

        def __init__(self, vpp_data, **kwargs):
            super().__init__(vpp_data, **kwargs)
            self.data = vpp_data

        def _evaluate(self, x, out, *args, **kwargs):

            out['F'] = np.array([ - vpp_func_PO1(x, self.data, Ns)])
            out['G'] = const_PO1(x, self.data)

    problem = MyProblem(vpp_data,
                        n_var = nvars,
                        n_obj = 1,
                        n_ieq_constr = n_constr_ieq,
                        xl = lb,
                        xu = ub
                        )
    
    algorithm = GA(pop_size = 4)
    termination = (('n_gen', 1))

    from pymoo.constraints.as_penalty import ConstraintsAsPenalty
    from pymoo.core.evaluator import Evaluator
    from pymoo.core.individual import Individual

    res = minimize(ConstraintsAsPenalty(problem, penalty = 100.0), algorithm, termination, seed = 1, verbose = True)
    res = Evaluator().eval(problem, Individual(X = res.X))
    
    # res = minimize(problem, algorithm, termination, verbose = True, seed = 1)

    results = {}
    results['Lucro'] = res.F[0]
    x = res.X

    p_bm, p_dl, u_bm, u_dl = decomp_vetor_x(x, Nt, Nbm, Ndl)

    # print(f'\nO lucro dessa simulação é {- res.F[0]:.2f} R$')
    # print(f'\nO total de violação foi {res.CV[0]} R$')

    results['p_bm'] = p_bm.reshape((Nbm, Nt))
    results['u_bm'] = u_bm.reshape((Nbm, Nt))
    results['p_dl'] = p_dl.reshape((Ndl, Nt))
    results['u_dl'] = u_dl.reshape((Ndl, Nt))


    return results, x
