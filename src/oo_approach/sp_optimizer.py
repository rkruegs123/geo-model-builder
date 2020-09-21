import pdb
import collections
import random
import sympy as sp
import itertools
from scipy.optimize import minimize
from math import tanh, cos, sin, acos, sqrt, exp
import signal
import re

from oo_approach.optimizer import Optimizer

def multisub(subs, subject):
    "Simultaneously perform all substitutions on the subject string."
    pattern = '|'.join('(%s)' % re.escape(p) for p, s in subs)
    substs = [s for p, s in subs]
    replace = lambda m: substs[m.lastindex - 1]
    return re.sub(pattern, replace, subject)

def handler(signum, frame):
    print("Simplification failed!")
    raise Exception("Timeout!")

signal.signal(signal.SIGALRM, handler)

# FIXME: Could call simplify in __init__
class SpPoint(collections.namedtuple("SpPoint", ["x", "y"])):
    def __add__(self, p):
        return SpPoint(self.x + p.x, self.y + p.y)
    def __sub__(self, p):
        return SpPoint(self.x - p.x, self.y - p.y)
    def smul(self, z):
        return SpPoint(self.x * z, self.y * z)
    def norm(self):
        return sp.sqrt(self.x**2 + self.y**2)


Init = collections.namedtuple("Init", ["name", "initialization", "args"])

class ScipyOptimizer(Optimizer):

    def __init__(self, instructions, opts):
        self.params = list()
        self.obj_fun = ""

        super().__init__(instructions, opts)

    def get_point(self, x, y):
        return SpPoint(x, y)

    def simplify_aux(self, sp_expr, method, timeout=5):
        signal.alarm(timeout)
        if method == "all":
            simp = sp_expr.simplify()
        elif method == "trig":
            simp = sp.trigsimp(sp_expr)
        else:
            raise RuntimeError(f"[simplify_aux] unrecognized method: {method}")
        return simp

    def simplify(self, p, method="all"):
        try:
            simp_x = self.simplify_aux(p.x, method=method)
        except:
            simp_x = p.x
        signal.alarm(0) # Disable alarm
        try:
            simp_y = self.simplify_aux(p.y, method=method)
        except:
            simp_y = p.y
        signal.alarm(0) # Disable alarm
        return self.get_point(simp_x, simp_y)

    def mkvar(self, name, shape=[], lo=-1.0, hi=1.0, trainable=None):
        if shape != []:
            raise RuntimeError("[mkvar] Scipy mkvar cannot make more than one variable at once")
        if trainable:
            raise RuntimeError("[mkvar] Scipy mkvar cannot make variable not trainable (yet)")
        self.params.append(Init(name, "uniform", [lo, hi]))
        return sp.Symbol(name, real=True)

    def register_pt(self, p, P):
        assert(p not in self.name2pt)
        # self.name2pt[p] = P.simplify()
        self.name2pt[p] = P


    # Note that weight not relevant for scipy
    def register_loss(self, key, val, weight=1.0):
        assert(key not in self.losses)

        val = self.param_str_2_sp_str(str(val))
        # Note that in tensorflow, we'd be minimizing val**2
        scipy_constraint = { 'type': 'eq', 'fun': self.get_scipy_lambda(val) }
        self.losses[key] = scipy_constraint
        self.has_loss = True

    def regularize_points(self):
        norms = [p.norm() for p in self.name2pt.values()]
        # summed_norms = self.sumVs(norms)
        mean_norm = self.sumVs(norms) / len(norms)
        # self.add_to_objective(f"{self.opts.regularize_points} * {summed_norms}")
        self.add_to_objective(f"{self.opts.regularize_points} * {mean_norm}")

    def make_points_distinct(self):
        if random.random() < self.opts.distinct_prob:
            sqdists = [self.sqdist(A, B) for A, B in itertools.combinations(self.name2pt.values(), 2)]
            mean_sqdist = self.sumVs(sqdists) / len(sqdists)
            # summed_sqdists = self.sumVs(sqdists)
            # self.add_to_objective(f"{self.opts.make_distinct} * {summed_sqdists}")
            self.add_to_objective(f"{self.opts.make_distinct} * {mean_sqdist}")


    #####################
    ## Math Utilities
    ####################
    def sum(self, xs):
        return sum(xs)

    def sqrt(self, x):
        return sp.sqrt(x)

    def sin(self, x):
        return sp.sin(x)

    def cos(self, x):
        return sp.cos(x)

    def acos(self, x):
        return sp.acos(x)

    def tanh(self, x):
        return sp.tanh(x)

    def sigmoid(self, x):
        return 1 / (1 + sp.exp(-x))

    def const(self, x):
        return x

    def max(self, x, y):
        return sp.Max(x, y)

    def cond(self, cond, t_val, f_val):
        return sp.Piecewise((t_val, cond), (f_val, True))

    def lt(self, x, y):
        return x < y

    def lte(self, x, y):
        return x <= y

    def gt(self, x, y):
        return x > y

    def gte(self, x, y):
        return x >= y

    def abs(self, x, y):
        return sp.Abs(x)


    #####################
    ## Scipy Utilities
    ####################

    def get_scipy_lambda(self, fun_str):
        return lambda x: eval(fun_str)

    def add_to_objective(self, expr_str):
        if self.obj_fun:
            self.obj_fun += f"+ {expr_str}"
        else:
            self.obj_fun = expr_str

    def param_str_2_sp_str(self, pstr):

        replace_map = [
            ("Abs", "abs")
        ]
        replace_map += [(param.name, f"x[{i}]") for i, param in enumerate(self.params)]

        scipy_str = multisub(replace_map, pstr)

        '''
        scipy_str = pstr
        for i, param in enumerate(self.params):
            p_name = param.name
            scipy_str = scipy_str.replace(p_name, f"x[{i}]")
        '''
        return scipy_str

    #####################
    ## Core
    ####################

    def sample_inits(self):
        inits = list()

        for p in self.params:
            if not isinstance(p, Init):
                raise RuntimeError("[sample_inits] Param not init")
            name, init_method, init_args = p
            if init_method == "uniform":
                [lo, hi] = init_args
                val = random.uniform(lo, hi)
                inits.append((name, val))
        return inits


    def get_point_assignment(self, model):
        # FIXME: Make cleaner -- shouldn't have to convert to dict here
        model = { sp.Symbol(p_name, real=True) : val for (p_name, val) in model }
        pt_assn = dict()
        for pt_name, pt in self.name2pt.items():
            px = pt.x if isinstance(pt.x, float) else pt.x.subs(model)
            py = pt.y if isinstance(pt.y, float) else pt.y.subs(model)
            if not (isinstance(px, sp.Number) or type(px) == float) or not (isinstance(py, sp.Number) or type(py) == float):
                raise RuntimeError("Failed evaluation")
            pt_assn[pt_name] = SpPoint(float(px), float(py))
        return pt_assn

    def solve(self):
        if self.has_loss:
            self.regularize_points()
            self.make_points_distinct()

        assignments = list()
        for _ in range(self.opts.n_tries):
            inits = self.sample_inits()
            if not self.has_loss:
                assignment = self.get_point_assignment(inits)
                assignments.append(assignment)
            else:
                if not self.obj_fun:
                    objective_fun = self.get_scipy_lambda("0")
                else:
                    scipy_obj_fun = self.param_str_2_sp_str(self.obj_fun)
                    objective_fun = self.get_scipy_lambda(scipy_obj_fun)
                init_vals = [x[1] for x in inits]
                cons = [c for c in self.losses.values()]

                # res = minimize(objective_fun, init_vals, constraints=cons, options={'ftol': 1e-2, 'disp': True, 'iprint': 99, 'eps': 1.5e-8, 'maxiter': 300}, method="SLSQP")
                res = minimize(objective_fun, init_vals, constraints=cons, options={'xtol': 1e-5, 'gtol': 1e-2, 'verbose': 3}, method="trust-constr")

                print(res)

                if res.success:
                    solved_vals = [(init.name, val) for (init, val) in zip(self.params, res.x)]
                    assignment = self.get_point_assignment(solved_vals)
                    assignments.append(assignment)
        return assignments




'''
TODOS:
-Add assertion support, try more problems
-See if simplification gets scipy to work for hexagon
-Play with tolerances and step sizes for scipy
-Add verbosity
-Generalize eps to any optimizer?
-Understand meaning of scipy metrics. For example, is constraint violation total or average?
-Simplify constraints before registering them?
'''

'''
Notes:
- err isn't squared for scipy -- regularization and distinctness are enforced much differently than for tensorflow
'''
