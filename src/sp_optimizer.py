import pdb
import collections
import random
import sympy as sp
import itertools
from scipy.optimize import minimize
from math import tanh, cos, sin, acos, sqrt, exp
import signal
import re

from optimizer import Optimizer
from diagram import Diagram

# Can we now get rid of simpliification given lambdify!?

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
        self.obj_fun = None

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
        self.losses[key] = val
        self.has_loss = True

    # Note that NDGs will have non-zero value in scipy whereas in tensorflow their losses will be 0 (for satisfied NDGs)
    def register_ndg(self, key, val, weight=1.0):
        assert(key not in self.ndgs)
        self.ndgs[key] = val

    def register_goal(self, key, val):
        assert(key not in self.goals)
        self.goals[key] = val

    def regularize_points(self):
        norms = [p.norm() for p in self.name2pt.values()]
        # summed_norms = self.sumVs(norms)
        mean_norm = self.sum(norms) / len(norms)
        self.update_objective(self.opts.regularize_points * mean_norm)

    def make_points_distinct(self):
        if random.random() < self.opts.distinct_prob:
            sqdists = [self.sqdist(A, B) for A, B in itertools.combinations(self.name2pt.values(), 2)]
            mean_sqdist = self.sum(sqdists) / len(sqdists)
            # summed_sqdists = self.sumVs(sqdists)
            self.update_objective(self.opts.make_distinct * mean_sqdist)


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

        if isinstance(t_val, SpPoint):
            tx, ty = t_val
            fx, fy = f_val

            return self.get_point(
                sp.Piecewise((tx, cond), (fx, True)),
                sp.Piecewise((ty, cond), (fy, True))
            )
        elif isinstance(t_val, list):
            return [self.cond(cond, t, f) for (t, f) in zip(t_val, f_val)]
        return sp.Piecewise((t_val, cond), (f_val, True))

    def lt(self, x, y):
        return x < y

    def lte(self, x, y):
        return x <= y

    def gt(self, x, y):
        return x > y

    def gte(self, x, y):
        return x >= y

    def logical_or(self, x, y):
        return sp.Or(x, y)

    def abs(self, x):
        return sp.Abs(x)

    def exp(self, x):
        return sp.exp(x)


    #####################
    ## Scipy Utilities
    ####################

    def update_objective(self, sp_expr):
        if self.obj_fun:
            self.obj_fun += sp_expr
        else:
            self.obj_fun = sp_expr

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

    def params2point(self, p, solved_params):
        px = p.x if isinstance(p.x, float) else p.x.subs(solved_params)
        py = p.y if isinstance(p.y, float) else p.y.subs(solved_params)

        if not (isinstance(px, sp.Number) or type(px) == float) or not (isinstance(py, sp.Number) or type(py) == float):
            raise RuntimeError("[params2point] Failed evaluation")
        return self.get_point(float(px), float(py))

    def get_model(self, solved_params):
        # FIXME: Make cleaner -- shouldn't have to convert to dict here
        solved_params = { sp.Symbol(p_name, real=True) : val for (p_name, val) in solved_params }
        pt_assn = dict()
        for pt_name, pt in self.name2pt.items():
            pt_assn[pt_name] = self.params2point(pt, solved_params)
        segments = [(self.params2point(sa, solved_params), self.params2point(sb, solved_params)) for (sa, sb) in self.segments]
        circles = [(self.params2point(sO, solved_params), sr.subs(solved_params)) for (sO, sr) in self.circles]
        ndgs = { key: val.subs(solved_params) for key, val in self.ndgs.items()  }
        goals = { key: val.subs(solved_params) for key, val in self.goals.items()  }
        return Diagram(points=pt_assn, segments=segments, circles=circles, ndgs=ndgs, goals=goals)

    def solve(self):

        if self.has_loss:
            self.regularize_points()
            self.make_points_distinct()

            # We wanted to wait until all the params are populated!
            lambdified_losses = dict()
            x = tuple([sp.Symbol(p.name, real=True) for p in self.params])
            for key, loss_expr in self.losses.items():
                loss_lambda = sp.lambdify([x], loss_expr)
                lambdified_losses[key] = { 'type': 'eq', 'fun': loss_lambda }

            # Note that the actual ndg_loss value is ignored in this optimizer
            if self.opts.ndg_loss > 0:
                # Inequalitiy constraints in scipy are for non-negativity (val >= 0)
                for key, ndg_expr in self.ndgs.items():
                    ndg_expr = self.abs(ndg_expr) - 1e-2
                    ndg_lambda = sp.lambdify([x], ndg_expr)
                    lambdified_losses[key] = { 'type': 'ineq', 'fun': ndg_lambda }


            if not self.obj_fun:
                self.obj_fun = sp.sympify(0)
            objective_fun = sp.lambdify([x], self.obj_fun)


        models = list()
        for _ in range(self.opts.n_tries):
            inits = self.sample_inits()
            if not self.has_loss:
                model = self.get_model(inits)
                if self.points_far_enough_away(model.points, self.opts.min_dist):
                    models.append(model)
            else:
                init_vals = [x[1] for x in inits]
                cons = [c for c in lambdified_losses.values()]

                # res = minimize(objective_fun, init_vals, constraints=cons, options={'ftol': 1e-2, 'disp': True, 'iprint': 99, 'eps': 1.5e-8, 'maxiter': 300}, method="SLSQP")
                res = minimize(objective_fun, init_vals, constraints=cons, options={'xtol': 1e-5, 'gtol': 1e-2, 'verbose': 3}, method="trust-constr")

                print(res)

                if res.success:
                    solved_vals = [(init.name, val) for (init, val) in zip(self.params, res.x)]
                    model = self.get_model(solved_vals)
                    if self.points_far_enough_away(model.points, self.opts.min_dist):
                        models.append(model)
        return models
