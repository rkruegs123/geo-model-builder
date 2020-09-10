from abc import ABC, abstractmethod
import math
import pdb

from instruction import *

class Optimizer(ABC):
    def __init__(self, instructions, opts):

        self.name2pt = dict()
        self.losses = dict()
        self.has_loss = False
        self.opts = opts
        self.instructions = instructions

        super().__init__()

        # self.preprocess()

    def preprocess(self):
        for i in self.instructions:
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

    @abstractmethod
    def get_point(self, x, y):
        pass

    def lookup_pts(self, ps):
        return [self.name2pt[p] for p in ps]

    @abstractmethod
    def mkvar(self, name, shape=[], lo=-1.0, hi=1.0, trainable=None):
        pass

    @abstractmethod
    def register_pt(self, p, P):
        pass

    @abstractmethod
    def register_loss(self, key, var, weight=1.0):
        pass


    @abstractmethod
    def regularize_points(self):
        pass

    @abstractmethod
    def make_points_distinct(self):
        pass

    # FIXME: The below should be combined with an abstract Point class

    #####################
    ## Math Utilities
    ####################
    @abstractmethod
    def addV(self, x, y):
        pass

    @abstractmethod
    def subV(self, x, y):
        pass

    @abstractmethod
    def negV(self, x):
        pass

    @abstractmethod
    def sumVs(self, xs):
        pass

    @abstractmethod
    def mulV(self, x, y):
        pass

    @abstractmethod
    def divV(self, x, y):
        pass

    @abstractmethod
    def powV(self, x, y):
        pass

    @abstractmethod
    def sinV(self, x):
        pass

    @abstractmethod
    def cosV(self, x):
        pass

    @abstractmethod
    def acosV(self, x):
        pass

    @abstractmethod
    def tanhV(self, x):
        pass

    @abstractmethod
    def constV(self, x):
        pass

    #####################
    ## Sample
    ####################

    def sample(self, i):
        sampling_method = i.sampler
        if sampling_method == "uniform":
            self.sample_uniform(i.points)
        elif sampling_method == "polygon":
            self.sample_polygon(i.points)
        else:
            raise NotImplementedError("FIXME: Finish sample")

    def sample_uniform(self, ps):
        [p] = ps
        P   = self.get_point(x=self.mkvar(p+"x"), y=self.mkvar(p+"y"))
        self.register_pt(p, P)


    def sample_polygon(self, ps):
        if len(ps) < 4:
            print("WARNING: sample_polygon expecting >3 points")

        angle_zs = [self.mkvar(name=f"polygon_angle_zs_{i}") for i in range(len(ps))]
        multiplicand = ((len(ps) - 2) / len(ps)) * math.pi + (math.pi / 3)
        angles = [self.mulV(multiplicand, self.tanhV(self.mulV(0.2, az))) for az in angle_zs]

        scale_zs = [self.mkvar(name=f"polygon_scale_zs_{i}") for i in range(len(ps))]
        scales = [self.mulV(0.5, self.tanhV(self.mulV(0.2, sz))) for sz in scale_zs]

        Ps = [self.get_point(self.constV(-2.0), self.constV(0.0)),
              self.get_point(self.constV(2.0), self.constV(0.0))]
        s = self.dist(Ps[0], Ps[1])

        for i in range(2, len(ps) + 1):
            A, B = Ps[-2:]
            X = B + self.rotate_counterclockwise(self.negV(angles[i-1]), A - B)
            scale = self.divV(self.mulV(s, self.addV(1, scales[i-1])), self.dist(X, B))
            P = B + (X - B).smul(scale)
            Ps.append(P)

        # Angles should sum to (n-2) * pi
        angle_sum = self.sumVs(angles)
        expected_angle_sum = math.pi * (len(ps) - 2)
        self.register_loss("polygon-angle-sum", self.subV(angle_sum, expected_angle_sum), weight=1e-1)

        # First point shoudl equal the last point
        self.register_loss("polygon-first-eq-last", self.dist(Ps[0], Ps[len(ps)]), weight=1e-2)

        # First angle should be the one sampled (known to be <180)
        self.register_loss("polygon-first-angle-eq-sampled",
                           self.subV(angles[0], self.angle(Ps[-1], Ps[0], Ps[1])),
                           weight=1e-2)


        for p, P in zip(ps, Ps[:-1]):
            self.register_pt(p, P)


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
        M = self.midp(A, B)
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

    def parameterize_coords(self, p):
        self.sample_uniform([p])

    #####################
    ## Comp. Geo
    ####################

    def midp(self, A, B):
        return (A + B).smul(0.5)

    def sqdist(self, A, B):
        xdiff = self.subV(A.x, B.x)
        ydiff = self.subV(A.y, B.y)
        return self.addV(self.powV(xdiff, 2), self.powV(ydiff, 2))

    def dist(self, A, B):
        return self.powV(self.sqdist(A,B), 0.5)

    def inner_product(self, A, B):
        a1, a2 = A
        b1, b2 = B
        return self.addV(self.mulV(a1, b1), self.mulV(a2, b2))

    def matrix_mul(self, mat, pt):
        pt1, pt2 = mat
        return self.get_point(self.inner_product(pt1, pt), self.inner_product(pt2, pt))

    def rotation_matrix(self, theta):
        r1 = self.get_point(self.cosV(theta), self.negV(self.sinV(theta)))
        r2 = self.get_point(self.sinV(theta), self.cosV(theta))
        return (r1, r2)

    def rotate_counterclockwise(self, theta, pt):
        return self.matrix_mul(self.rotation_matrix(theta), pt)

    def side_lengths(self, A, B, C):
        return self.dist(B, C), self.dist(C, A), self.dist(A, B)

    def angle(self, A, B, C):
        a, b, c = self.side_lengths(A, B, C)
        num = self.subV(self.addV(self.powV(a, 2), self.powV(c, 2)), self.powV(b, 2))
        denom = self.mulV(self.mulV(a, 2), c)
        return self.acosV(self.divV(num, denom))
