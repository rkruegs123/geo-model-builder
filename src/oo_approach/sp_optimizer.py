import tensorflow.compat.v1 as tf
import pdb
import collections
import random
import sympy as sp

from oo_approach.optimizer import Optimizer

# FIXME: Could call simplify in __init__
class ScpPoint(collections.namedtuple("ScpPoint", ["x", "y"])):
    def __add__(self, p):
        return ScpPoint(f"({self.x}) + ({p.x})", f"({self.y}) + ({p.y})")
    def __sub__(self, p):
        return ScpPoint(f"({self.x}) - ({p.x})", f"({self.y}) - ({p.y})")
    def smul(self, z):
        return ScpPoint(f"({self.x}) * ({z})", f"({self.y}) * ({z})")

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

        super().__init__(instructions, opts)

    def get_point(self, x, y):
        return ScpPoint(x, y)

    def mkvar(self, name, shape=[], lo=-1.0, hi=1.0, trainable=False):
        if shape != []:
            raise RuntimeError("[mkvar] Scipy mkvar cannot make more than one variable at once")
        if trainable:
            raise RuntimeError("[mkvar] Scipy mkvar cannot make variable not trainable (yet)")
        self.params.append(Init(name, "uniform", [lo, hi]))
        return name

    def register_pt(self, p, P):
        assert(p not in self.name2pt)
        self.name2pt[p] = P.simplify()

    #####################
    ## Math Utilities
    ####################
    def addV(self, x, y):
        return f"({x}) + ({y})"

    def subV(self, x, y):
        return f"({x}) - ({y})"

    def negV(self, x):
        return f"(-{x})"

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

    def tanhV(self, x):
        return f"tanh({x})"

    def constV(self, x):
        return str(x)


    #####################
    ## Scipy Utilities
    ####################

    #####################
    ## Sample
    ####################

    '''
    def sample_uniform(self, ps):
        [p] = ps
        xvar, yvar = f"{p}x", f"{p}y"
        self.params.extend([Init(xvar, "uniform", [-1.0, 1.0]), Init(yvar, "uniform", [-1.0, 1.0])])
        P = self.get_point(xvar, yvar)
        self.name2pt[p] = P
    '''

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
            raise NotImplementedError("[scp_optimizer.solve] Cannot solve with loss")

        assignments = list()
        for _ in range(self.opts.n_tries):
            if not self.has_loss:

                inits = self.sample_inits()
                assignment = self.get_point_assignment(inits)
                assignments.append(assignment)
        return assignments
