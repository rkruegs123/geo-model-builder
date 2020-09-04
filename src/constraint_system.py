import collections
from instruction import *

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

'''

Loss = collections.namedtuple("Loss", ["expr", "weight", "hard"])

Init = collections.namedtuple("Init", ["initialization"])
Expr = collections.namedtuple("Expr", ["op", "args"])

class Point(collections.namedtuple("Point", ["x", "y"])):
    def __add__(self, p):
        return Point(
            x=Expr("add", [self.x, p.x]),
            y=Expr("add", [self.y, p.y])
        )

    def smul(self, z):
        return Point(
            x=Expr("mul", [self.x, z]),
            y=Expr("mul", [self.y, z])
        )

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

    def sample_uniform(self, ps):
        [p] = ps
        P = Point(x=Init("uniform"), y=Init("uniform"))
        self.name2pt[p] = P

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

        raise NotImplementedError("FIXME: Finish compute_midp")


    #####################
    ## Parameterize
    ####################

    def parameterize(self, i):
        param_method = i.parameterization
        if param_method == "coords":
            self.parameterize_coords(i.point)
        else:
            raise NotImplementedError("FIXME: Finish parameterize")

    def parameterize_coords(self, p):
        xvar, yvar = f"{p}x", f"{p}y"
        self.params.extend([xvar, yvar])
        P = Point(x=xvar, y=yvar)
        self.name2pt[p] = P

    #####################
    ## Computational Geometry
    ####################

    def midp(self, A, B):
        return (A + B).smul(0.5)

    #####################
    ## Utility
    ####################

    def lookup_pts(self, ps):
        return [self.name2pt[p] for p in ps]
