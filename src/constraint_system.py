import collections
import math

from instruction import *
from comp_geo import *

'''
PCoords a
PCoords b
Compute x (midp a b)

---->

-params will either be Init or Op
-for tensorflow, all points can be added to the computation graph and just run to check
-for scipy, we will prob. just want to evaluate the grammar manually (no computation graph). a really fancy way would be using tensorflow for evaluation...


params = [ax, ay, bx, by]
points = [(ax, ay), (bx, by), ((ax + bx) / 2, (ay + by) / 2)]
losses = []

Tensorflow:
-make variables to each parameter
-run with global initializer
-run with points
-check points far away enough

Scipy:
-if no constraints, just initialize (sample), and do your checks
-if constraints, translate parametrs to a vector, make strings out of the losses with appropriate indices, either turn to objective function or otherwise, then optimize

-will have to CHECK model by explicit substitution, unfortunately

api will look something like:
scipy_solve(constraint_system, n_models)
tf_solve(constraint_system, n_models)




self.params should store Inits --


'''

Loss = collections.namedtuple("Loss", ["name", "expr", "weight", "hard"])

# Used to represent variables in a constraint system
Init = collections.namedtuple("Init", ["name", "initialization", "args"])

# Used as references to variables in a constraint system
def var(name):
    return Expr("var", [name])

#####################
## Constraint System
####################

class ConstraintSystem:
    def __init__(self, instructions):
        self.instructions = instructions
        self.name2pt = {}
        self.params = list()
        self.losses = list()

        for i in instructions:
            self.process_instruction(i)

    def process_instruction(self, i):
        if isinstance(i, Sample):
            self.sample(i)
        elif isinstance(i, Compute):
            self.compute(i)
        elif isinstance(i, Parameterize):
            self.parameterize(i)
        else:
            raise NotImplementedError("FIXME: Finish process_instruction")

    #####################
    ## Sample
    ####################

    def sample(self, i):
        sampling_method = i.sampler
        if sampling_method == "uniform":
            self.sample_uniform(i.points)
        else:
            raise NotImplementedError("FIXME: Finish sample")

    # FIXME: Currently all vars will be trainable!
    def sample_uniform(self, ps, lo=-1.0, hi=1.0):
        [p] = ps
        xvar, yvar = f"{p}x", f"{p}y"
        self.params.extend([Init(xvar, "uniform", [lo, hi]), Init(yvar, "uniform", [lo, hi])])
        P = Point(x=var(xvar), y=var(yvar))
        self.name2pt[p] = P


    def sample_polygon(self, ps):
        if len(ps) < 4:
            print("WARNING: sample_polygon expecting >3 points")

        angle_zs = [Init(f"polygon_angle_z{i}", "uniform", [-1.0, 1.0]) for i in range(len(ps))]
        self.params.extend(angle_zs)
        angles = list()
        multiplicand = const(((len(ps) - 2) / len(ps)) * math.pi + (math.pi / 3))
        for az in angle_zs:
            ang = multiplicand * Expr("tanh", const(0.2) * var(az.name))
            angles.append(ang)

        scale_zs = [Init(f"polygon_scale_z{i}", "uniform", [-1.0, 1.0]) for i in range(len(ps))]
        self.params.extend(scale_zs)
        scales = list()
        for sz in scale_zs:
            scale = const(0.5) * Expr("tanh", [const(0.2) * var(sz.name)])
            scales.append(scale)

        Ps = [Point(x=const(-2.0), y=const(0.0)), Point(x=const(2.0), y=const(0.0))]
        s = dist(Ps[0], Ps[1])

        for i in range(2, len(ps) + 1):
            A, B = Ps[-2:]
            X    = B + rotate_counterclockwise(-angles[i-1], A - B)
            P    = B + (X - B).smul(s * (1 + scales[i-1]) / dist(X, B))
            Ps.append(P)

        # Record losses
        polygon_angle_sum_loss = Expr("sum", angles) - const(math.pi * (len(ps) - 2))
        self.losses.append(Loss("polygon-angle-sum", polygon_angle_sum_loss, 1e-1, True))

        polygon_first_eq_last = dist(Ps[0], Ps[len(ps)])
        self.losses.append(Loss("polygon-first-eq-last", polygon_first_eq_last, 1e-2, True))

        polygon_first_angle_eq_sampled = angles[0] - angle(Ps[-1], Ps[0], Ps[1])
        self.losses.append(Loss("polygon-first-angle-eq-sampled", polygon_first_angle_eq_sampled, 1e-2, True))

        # Register points
        for p, P in zip(ps, Ps[:-1]):
            self.name2pt[p] = P



    def sample_triangle(self, ps, iso=None, right=None, acute=False, equi=False):
        if not (iso or right or acute or equi):
            return self.sample_polygon(ps)

        [nA, nB, nC] = ps
        B = Point(x=const(-2.0), y=const(0.0))
        C = Point(x=const(2.0), y=const(0.0))

        if iso is not None or equi:
            Ax = const(0.0)
        else:
            Ax = Init("tri_x", "uniform", [-1.2, 1.2])


        if right is not None:
            Ay = Expr("sqrt", [const(4) - (Ax ** 2)])
        elif equi:
            Ay = const(2) * Expr("sqrt", [const(3)])
        else:
            aylo = 1.1 if acute else 0.4
            z = Init("tri", "uniform", [-1.0, 1.0])
            self.params.append(z)
            Ay = const(aylo) + const(3.0) * Expr("sigmoid", [var("tri")])

        A = Point(x=Ax, y=Ay)

        # Shuffle, if the isosceles vertex was not C
        if iso == nB or right == nB:   (A, B, C) = (B, A, C)
        elif iso == nC or right == nC: (A, B, C) = (C, B, A)

        self.name2pt[nA] = A
        self.name2pt[nB] = B
        self.name2pt[nC] = C

    #####################
    ## Compute
    ####################

    def compute(self, i):
        if i.computation[0] == "midp":
            self.compute_midp(i.point, i.computation[1])
        else:
            raise NotImplementedError("FIXME: Finish compute")

    def compute_midp(self, m, ps):
        A, B = self.lookup_pts(ps)
        M = midp(A, B)
        self.name2pt[m] = M


    #####################
    ## Parameterize
    ####################

    def parameterize(self, i):
        param_method = i.parameterization
        if param_method == "coords":
            self.parameterize_coords(i.point)
        else:
            raise NotImplementedError("FIXME: Finish parameterize")

    # def sample_uniform(self, ps, lo=-1.0, hi=1.0):
    def parameterize_coords(self, p):
        self.sample_uniform([p])


    #####################
    ## Utility
    ####################

    def lookup_pts(self, ps):
        return [self.name2pt[p] for p in ps]
