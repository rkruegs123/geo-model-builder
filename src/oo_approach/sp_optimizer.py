import tensorflow.compat.v1 as tf
import pdb
import collections
import random
import sympy as sp
import itertools
from scipy.optimize import minimize
from math import tanh, cos, sin, acos, sqrt

from oo_approach.optimizer import Optimizer

# FIXME: Could call simplify in __init__
class ScpPoint(collections.namedtuple("ScpPoint", ["x", "y"])):
    def __add__(self, p):
        return ScpPoint(f"({self.x}) + ({p.x})", f"({self.y}) + ({p.y})")
    def __sub__(self, p):
        return ScpPoint(f"({self.x}) - ({p.x})", f"({self.y}) - ({p.y})")
    def smul(self, z):
        return ScpPoint(f"({self.x}) * ({z})", f"({self.y}) * ({z})")
    def norm(self):
        return f"sqrt(({self.x})**2 + ({self.y})**2)"

    # TODO: Try simplify, and if it takes too long, revert to sympify
    def simplify(self):
        # simpX = str(sp.sympify(self.x).simplify())
        # simpY = str(sp.sympify(self.y).simplify())
        simpX = str(sp.sympify(self.x))
        simpY = str(sp.sympify(self.y))
        return ScpPoint(simpX, simpY)


Init = collections.namedtuple("Init", ["name", "initialization", "args"])

class ScpOptimizer(Optimizer):

    def __init__(self, instructions, opts):
        self.params = list()
        self.obj_fun = ""

        super().__init__(instructions, opts)

    def get_point(self, x, y):
        return ScpPoint(x, y)

    def mkvar(self, name, shape=[], lo=-1.0, hi=1.0, trainable=None):
        if shape != []:
            raise RuntimeError("[mkvar] Scipy mkvar cannot make more than one variable at once")
        if trainable:
            raise RuntimeError("[mkvar] Scipy mkvar cannot make variable not trainable (yet)")
        self.params.append(Init(name, "uniform", [lo, hi]))
        return name

    def register_pt(self, p, P):
        assert(p not in self.name2pt)
        self.name2pt[p] = P.simplify()


    # Note that weight not relevant for scipy
    def register_loss(self, key, val, weight=1.0):
        assert(key not in self.losses)

        val = self.param_str_2_scipy_str(val)
        # Note that in tensorflow, we'd be minimizing val**2
        scipy_constraint = { 'type': 'eq', 'fun': self.get_scipy_lambda(val) }
        self.losses[key] = scipy_constraint
        self.has_loss = True

    def regularize_points(self):
        norms = [p.norm() for p in self.name2pt.values()]
        summed_norms = self.sumVs(norms) # Note that in tensorflow we take the mean
        self.add_to_objective(f"{self.opts.regularize_points} * {summed_norms}")

    def make_points_distinct(self):
        if random.random() < self.opts.distinct_prob:
            # Note that in tensorflow we do something much different
            sqdists = [self.sqdist(A, B) for A, B in itertools.combinations(self.name2pt.values(), 2)]
            summed_sqdists = self.sumVs(sqdists)
            self.add_to_objective(f"{self.opts.make_distinct} * {summed_sqdists}")


    #####################
    ## Math Utilities
    ####################
    def addV(self, x, y):
        return f"({x}) + ({y})"

    def subV(self, x, y):
        return f"({x}) - ({y})"

    def negV(self, x):
        return f"(-{x})"

    def sumVs(self, xs):
        return f"sum([{', '.join(xs)}])"

    def mulV(self, x, y):
        return f"({x}) * ({y})"

    def divV(self, x, y):
        return f"({x}) / ({y})"

    def powV(self, x, y):
        return f"({x}) ** ({y})"

    def sinV(self, x):
        return f"sin({x})"

    def cosV(self, x):
        return f"cos({x})"

    def acosV(self, x):
        return f"acos({x})"

    def tanhV(self, x):
        return f"tanh({x})"

    def constV(self, x):
        return str(x)


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

    def param_str_2_scipy_str(self, pstr):
        scipy_str = pstr
        for i, param in enumerate(self.params):
            p_name = param.name
            scipy_str = scipy_str.replace(p_name, f"x[{i}]")
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
        pt_assn = dict()
        for pt_name, pt in self.name2pt.items():
            px = pt.x
            py = pt.y
            for (param_name, param_val) in model:
                px = px.replace(param_name, str(param_val))
                py = py.replace(param_name, str(param_val))
            px = sp.sympify(px).evalf()
            py = sp.sympify(py).evalf()
            pt_assn[pt_name] = ScpPoint(px, py)
        return pt_assn

    def solve(self):
        if self.has_loss:
            self.regularize_points()
            self.make_points_distinct()
            # raise NotImplementedError("[scp_optimizer.solve] Cannot solve with loss")

        assignments = list()
        for _ in range(self.opts.n_tries):
            inits = self.sample_inits()
            if not self.has_loss:
                assignment = self.get_point_assignment(inits)
                assignments.append(assignment)
            else:
                # FIXME: objective_fun with soft constraints
                if not self.obj_fun:
                    objective_fun = self.get_scipy_lambda("0")
                else:
                    scipy_obj_fun = self.param_str_2_scipy_str(self.obj_fun)
                    objective_fun = self.get_scipy_lambda(scipy_obj_fun)
                init_vals = [x[1] for x in inits]
                cons = [c for c in self.losses.values()]

                pdb.set_trace()
                # res = minimize(objective_fun, init_vals, constraints=cons, options={'ftol': 1e-1, 'disp': True, 'iprint': 99, 'eps': 1.5e-6})
                res = minimize(objective_fun, init_vals, constraints=cons, options={'xtol': 1e-2, 'gtol': 1e-2, 'verbose': 2}, method="trust-constr")


                print(res)

                if res.success:
                    solved_vals = [(init.name, val) for (init, val) in zip(self.params, res.x)]
                    assignment = self.get_point_assignment(solved_vals)
                    assignments.append(assignment)
        return assignments


# Check: is the constraint violation total or average? If total, tolerance can be higher...
# plot scipy results, see consequences of higher tolerances
# try scipy with 6 point polygon
# also try bigger step sizes
# add verbosity
# add regularization, etc for scipy
# try more problems
# make eps universal?

# make err squared for scipy
