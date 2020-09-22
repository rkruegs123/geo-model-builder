from abc import ABC, abstractmethod
import math
import pdb
import collections

from instruction import *

# Also stores the points used to compute it
SlopeInterceptForm = collections.namedtuple("SlopeInterceptForm", ["m", "b", "p1", "p2"])

CircleNF = collections.namedtuple("CircleNF", ["center", "radius"])

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
        elif isinstance(i, Assert):
            self.add(i)
        else:
            raise NotImplementedError("FIXME: Finish process_instruction")

    @abstractmethod
    def get_point(self, x, y):
        pass

    @abstractmethod
    def simplify(self, p, method="all"):
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
    def sum(self, xs):
        pass

    @abstractmethod
    def sqrt(self, x):
        pass

    @abstractmethod
    def sin(self, x):
        pass

    @abstractmethod
    def cos(self, x):
        pass

    @abstractmethod
    def acos(self, x):
        pass

    @abstractmethod
    def tanh(self, x):
        pass

    @abstractmethod
    def sigmoid(self, x):
        pass

    @abstractmethod
    def const(self, x):
        pass

    @abstractmethod
    def max(self, x, y):
        pass

    @abstractmethod
    def cond(self, cond, t_val, f_val):
        pass

    @abstractmethod
    def lt(self, x, y):
        pass

    @abstractmethod
    def lte(self, x, y):
        pass

    @abstractmethod
    def gt(self, x, y):
        pass

    @abstractmethod
    def gte(self, x, y):
        pass

    @abstractmethod
    def logical_or(self, x, y):
        pass

    @abstractmethod
    def abs(self, x):
        pass

    #####################
    ## Sample
    ####################

    def sample(self, i):
        s_method = i.sampler
        s_args = i.args
        if s_method == "uniform": self.sample_uniform(i.points)
        elif s_method == "polygon": self.sample_polygon(i.points)
        elif s_method == "triangle": self.sample_triangle(i.points)
        elif s_method == "isoTri": self.sample_triangle(i.points, iso=args[0])
        elif s_method == "acuteTri": self.sample_triangle(i.points, acute=True)
        elif s_method == "acuteIsoTri": self.sample_triangle(i.points, iso=args[0], acute=True)
        elif s_method == "rightTri": self.sample_triangle(i.points, right=args[0])
        elif s_method == "equiTri": self.sample_triangle(i.points, equi=True)
        else: raise NotImplementedError(f"[sample] NYI: Sampling method {s_method}")

    def sample_uniform(self, ps):
        [p] = ps
        P   = self.get_point(x=self.mkvar(p+"x"), y=self.mkvar(p+"y"))
        self.register_pt(p, P)


    def sample_polygon(self, ps):
        if len(ps) < 4:
            print("WARNING: sample_polygon expecting >3 points")

        angle_zs = [self.mkvar(name=f"polygon_angle_zs_{i}", lo=-0.5, hi=0.5) for i in range(len(ps))]
        multiplicand = ((len(ps) - 2) / len(ps)) * math.pi + (math.pi / 3)
        angles = [multiplicand * self.tanh(0.2 * az) for az in angle_zs]

        scale_zs = [self.mkvar(name=f"polygon_scale_zs_{i}") for i in range(len(ps))]
        scales = [0.5 * self.tanh(0.2 * sz) for sz in scale_zs]

        Ps = [self.get_point(self.const(-2.0), self.const(0.0)),
              self.get_point(self.const(2.0), self.const(0.0))]
        s = self.dist(Ps[0], Ps[1])

        for i in range(2, len(ps) + 1):
            # print(f"sampling polygon: {i}")
            A, B = Ps[-2:]
            X = B + self.rotate_counterclockwise(-angles[i-1], A - B)
            P = B + (X - B).smul(s * (1 + scales[i-1]) / self.dist(X, B))
            # Ps.append(P)
            Ps.append(self.simplify(P, method="trig"))

        # Angles should sum to (n-2) * pi
        angle_sum = self.sum(angles)
        expected_angle_sum = math.pi * (len(ps) - 2)
        self.register_loss("polygon-angle-sum", angle_sum - expected_angle_sum, weight=1e-1)

        # First point shoudl equal the last point
        self.register_loss("polygon-first-eq-last", self.dist(Ps[0], Ps[len(ps)]), weight=1e-2)

        # First angle should be the one sampled (known to be <180)
        self.register_loss("polygon-first-angle-eq-sampled",
                           angles[0] - self.angle(Ps[-1], Ps[0], Ps[1]),
                           weight=1e-2)

        for p, P in zip(ps, Ps[:-1]):
            self.register_pt(p, P)


    def sample_triangle(self, ps, iso=None, right=None, acute=False, equi=False):
        if not (iso or right or acute or equi):
            return self.sample_polygon(ps)

        [nA, nB, nC] = ps
        B = self.get_point(self.const(-2.0), self.const(0.0))
        C = self.get_point(self.const(2.0), self.const(0.0))

        if iso is not None or equi:
            Ax = self.const(0.0)
        else:
            Ax = self.mkvar("tri_x", lo=-1.0, hi=1.2)

        if right is not None:
            Ay = self.sqrt(4 - (Ax ** 2))
        elif equi:
            Ay = 2 * self.sqrt(self.const(3.0))
        else:
            AyLo = 1.1 if acute else 0.4
            z = self.mkvar("tri")
            Ay = self.const(AyLo) + 3.0 * self.sigmoid(z)

        A = self.get_point(Ax, Ay)

        # Shuffle if the isosceles vertex was not C
        if iso == nB or right == nB:   (A, B, C) = (B, A, C)
        elif iso == nC or right == nC: (A, B, C) = (C, B, A)

        self.register_pt(nA, A)
        self.register_pt(nB, B)
        self.register_pt(nC, C)



    #####################
    ## Compute
    ####################

    def compute(self, i):
        p = i.point
        c_method = i.computation[0]
        c_args = i.computation
        if c_method == "midp": self.compute_midp(p, c_args[1])
        elif c_method == "midpFrom": self.compute_midp_from(p, c_args[1])
        elif c_method == "amidpOpp": self.compute_amidp_opp(p, c_args[1])
        elif c_method == "amidpSame": self.compute_amidp_same(p, c_args[1])
        elif c_method == "circumcenter": self.compute_circumcenter(p, c_args[1])
        elif c_method == "incenter": self.compute_incenter(p, c_args[1])
        elif c_method == "excenter": self.compute_excenter(p, c_args[1])
        elif c_method == "orthocenter": self.compute_orthocenter(p, c_args[1])
        elif c_method == "centroid": self.compute_centroid(p, c_args[1])
        elif c_method == "interLL": self.compute_inter_ll(p, c_args[1], c_args[2])
        elif c_method == "interLC": self.compute_inter_lc(p, c_args[1], c_args[2], c_args[3])
        else: raise NotImplementedError(f"[compute] NYI: {c_method} not supported")

    def compute_midp(self, m, ps):
        A, B = self.lookup_pts(ps)
        M = self.midp(A, B)
        self.register_pt(m, M)

    def compute_midp_from(self, p, ps):
        M, A = self.lookup_pts(ps)
        P = self.midp_from(M, A)
        self.register_pt(p, P)

    def compute_amidp_opp(self, p, ps):
        B, C, A = self.lookup_pts(ps)
        P = self.amidp_opp(B, C, A)
        self.register_pt(p, P)

    def compute_amidp_same(self, p, ps):
        B, C, A = self.lookup_pts(ps)
        P = self.amidp_same(B, C, A)
        self.register_pt(p, P)

    def compute_circumcenter(self, o, ps):
        A, B, C = self.lookup_pts(ps)
        O = self.circumcenter(A, B, C)
        self.register_pt(o, O)

    def compute_orthocenter(self, h, ps):
        A, B, C = self.lookup_pts(ps)
        H = self.orthocenter(A, B, C)
        self.register_pt(h, H)

    def compute_centroid(self, g, ps):
        A, B, C = self.lookup_pts(ps)
        G = self.centroid(A, B, C)
        self.register_pt(g, G)

    def compute_incenter(self, i, ps):
        A, B, C = self.lookup_pts(ps)
        I = self.incenter(A, B, C)
        self.register_pt(i, I)

    def compute_excenter(self, i, ps):
        A, B, C = self.lookup_pts(ps)
        I = self.excenter(A, B, C)
        self.register_pt(i, I)

    def compute_inter_ll(self, p, l1, l2):
        sif1 = self.line2sif(l1)
        sif2 = self.line2sif(l2)
        P = self.inter_ll(sif1, sif2)
        self.register_pt(p, P)

    def compute_inter_lc(self, p, l, c, root_select):
        l_sif = self.line2sif(l)
        cnf = self.circ2nf(c)
        P = self.inter_lc(l_sif, cnf, root_select)
        self.make_lc_intersect(p, l_sif, cnf)
        self.register_pt(p, P)

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
    ## Assert
    ####################

    def add(self, i):
        assertion = i.constraint
        pred, ps, negate = assertion.pred, assertion.points, assertion.negate

        if negate:
            raise RuntimeError("[add] Mishandled negation")

        vals = self.assertion_vals(pred, ps)

        a_str = f"{pred}_{'_'.join(ps)}"
        weight = 1 / len(vals)
        for i, val in enumerate(vals):
            loss_str = a_str if len(vals) == 1 else f"a_str_{i}"
            self.register_loss(loss_str, val, weight=weight)

    def assertion_vals(self, pred, ps):
        if pred == "perp": return [self.perp_phi(*self.lookup_pts(ps))]
        elif pred == "para": return [self.para_phi(*self.lookup_pts(ps))]
        elif pred == "cong": return [self.cong_diff(*self.lookup_pts(ps))]
        elif pred == "midp":
            [M, A, B] = self.lookup_pts(ps)
            return [self.dist(M, self.midp(A, B))]
        else: raise NotImplementedError(f"[assertion_vals] NYI: {pred}")


    #####################
    ## Comp. Geo
    ####################

    def midp(self, A, B):
        return (A + B).smul(0.5)

    def midp_from(self, M, A):
        return A + (M - A).smul(2)

    def sqdist(self, A, B):
        return (A.x - B.x)**2 + (A.y - B.y)**2

    def dist(self, A, B):
        return self.sqdist(A, B) ** (1 / 2)

    def inner_product(self, A, B):
        a1, a2 = A
        b1, b2 = B
        return a1*b1 + a2*b2

    def matrix_mul(self, mat, pt):
        pt1, pt2 = mat
        return self.get_point(self.inner_product(pt1, pt), self.inner_product(pt2, pt))

    def rotation_matrix(self, theta):
        r1 = self.get_point(self.cos(theta), -self.sin(theta))
        r2 = self.get_point(self.sin(theta), self.cos(theta))
        return (r1, r2)

    def rotate_counterclockwise(self, theta, pt):
        return self.matrix_mul(self.rotation_matrix(theta), pt)

    def rotate_clockwise_90(self, pt):
        return self.matrix_mul(
            (self.get_point(self.const(0.0), self.const(1.0)),
             self.get_point(self.const(-1.0),self.const(0.0))),
            pt)

    def rotate_counterclockwise_90(self, pt):
        return self.matrix_mul(
            (self.get_point(self.const(0.0), self.const(-1.0)),
             self.get_point(self.const(1.0),self.const(0.0))),
            pt)

    def side_lengths(self, A, B, C):
        return self.dist(B, C), self.dist(C, A), self.dist(A, B)

    def angle(self, A, B, C):
        a, b, c = self.side_lengths(A, B, C)
        return self.acos((a**2 + c**2 - b**2) / (2 * a * c))

    def conway_vals(self, A, B, C):
        a, b, c = self.side_lengths(A, B, C)
        return (b**2 + c**2 - a**2)/2, (c**2 + a**2 - b**2)/2, (a**2 + b**2 - c**2)/2

    def trilinear(self, A, B, C, x, y, z):
        a, b, c = self.side_lengths(A, B, C)
        denom = a * x + b * y + c * z
        return self.get_point((a * x * A.x + b * y * B.x + c * z * C.x) / denom,
                              (a * x * A.y + b * y * B.y + c * z * C.y) / denom)

    def barycentric(self, A, B, C, x, y, z):
        a, b, c = self.side_lengths(A, B, C)
        return self.trilinear(A, B, C, x/a, y/b, z/c)

    def circumcenter(self, A, B, C):
        a, b, c = self.side_lengths(A, B, C)
        Sa, Sb, Sc = self.conway_vals(A, B, C)
        res = self.barycentric(A, B, C, a**2 * Sa, b**2 * Sb, c**2 * Sc)
        return res

    def orthocenter(self, A, B, C):
        a, b, c = self.side_lengths(A, B, C)
        Sa, Sb, Sc = self.conway_vals(A, B, C)
        return self.barycentric(A, B, C, Sb * Sc, Sc * Sa, Sa * Sb)

    def centroid(self, A, B, C):
        return self.barycentric(A, B, C, 1, 1, 1)

    def incenter(self, A, B, C):
        return self.trilinear(A, B, C, 1, 1, 1)

    def excenter(self, A, B, C):
        return self.trilinear(A, B, C, -1, 1, 1)

    def perp_phi(self, A, B, C, D):
        return (A.x - B.x) * (C.x - D.x) + (A.y - B.y) * (C.y - D.y)

    def para_phi(self, A, B, C, D):
        return (A.x - B.x) * (C.y - D.y) - (A.y - B.y) * (C.x - D.x)

    def cong_diff(self, A, B, C, D):
        return self.sqdist(A, B) - self.sqdist(C, D)

    def coll_phi(self, A, B, C):
        return A.x * (B.y - C.y) + B.x * (C.y - A.y) + C.x * (A.y - B.y)

    def between_gap(self, X, A, B):
        eps = 0.2

        def diff_signs(x, y):
            return self.max(self.const(0.0), x * y)

        A1 = self.get_point(A.x + eps * (B.x - A.x), A.y + eps * (B.y - A.y))
        B1 = self.get_point(B.x + eps * (A.x - B.x), B.y + eps * (A.y - B.y))

        return [diff_signs(X.x - A1.x, X.x - B1.x), diff_signs(X.y - A1.y, X.y - B1.y)]

    def det3(self, A, O, B):
        lhs = (A.x - O.x) * (B.y - O.y)
        rhs = (A.y - O.y) * (B.x - O.x)
        return lhs - rhs

    def side_score_prod(self, a, b, x, y):
        return self.det3(a, x, y) * self.det3(b, x, y)

    def opp_sides(self, a, b, x, y):
        return self.lt(self.side_score_prod(a, b, x, y), 0.0)

    def same_side(self, a, b, x, y):
        return self.gt(self.side_score_prod(a, b, x, y), 0.0)

    def inter_ll(self, sif1, sif2):
        (m1, b1) = sif1
        (m2, b2) = sif2

        px = (b2 - b1) / (m1 - m2)
        py = m1 * px + b1
        return self.get_point(px, py)

    def inter_pp_c(self, p1, p2, cnf):
        # We follow http://mathworld.wolfram.com/Circle-LineIntersection.html
        O, r = cnf
        P1, P2 = self.shift(O, [P1, P2])

        dx = P1.x - P2.x
        dy = P1.y - P2.y

        dr = self.sqrt(dx**2 + dy**2)
        D = P2.x * P1.y - P1.x * P2.y

        radicand = r**2 * dr**2 - D**2

        def on_nneg():
            def sgnstar(x):
                return self.cond(self.lt(x, self.const(0.0)), self.const(-1.0), self.const(1.0))

            # NEXT: Change to self....
            Q1 = self.get_point((D * dy + sgnstar(dy) * dx * self.sqrt(radicand)) / (dr**2),
                                (-D * dx + self.abs(dy) * self.sqrt(radicand)) / (dr**2))

            Q2 = self.get_point((D * dy - sgnstar(dy) * dx * self.sqrt(radicand)) / (dr**2),
                                (-D * dx - self.abs(dy) * self.sqrt(radicand)) / (dr**2))
            return self.unshift(O, [Q1, Q2])

        def on_neg():
            Operp = self.rotate_counterclockwise_90(P1 - P2) + O
            F = self.inter_ll(self.pp2sif(P1, P2), self.pp2sif(O, Operp))
            X = O + (F - O).smul(r / self.dist(O, F))
            Q = self.midp(F, X)
            return self.unshift(O, [Q, Q])

        return self.cond(self.less(radicand, self.const(0.0)), on_neg(), on_nneg())

    def inter_lc(self, l, c, root_select):
        p1, p2 = l.p1, l.p2
        I1, I2 = self.inter_pp_c(p1, p2, c)
        return self.process_rs(P1, P2, root_select)

    def make_lc_intersect(self, name, l, c):
        A, B = l.pp()
        O, r = c
        Operp = self.rotate_counterclockwise_90(A - B) + O

        F = self.inter_ll(l, self.pp2sif(O, Operp))
        d = self.dist(O, F)
        f_val = self.cond(self.less(r, d), d, self.const(0.0))

        loss = self.cond(self.logical_or(self.less(self.dist(O, Operp), 1e-6),
                                         self.less(self.dist(A, B), 1e-6)),
                         self.const(0.0), f_val)
        self.register_loss(f"interLC_{name}", [loss], weight=1e-1)

    def second_meet_pp_c(self, A, B, O):
        P1, P2 = self.inter_pp_c(A, B, CircleNF(O, self.dist(O, A)))
        return self.cond(self.less(self.sqdist(A, P1), self.sqdist(A, P2)), P2, P1)

    def amidp_opp(self, B, C, A):
        O = self.circumcenter(A, B, C)
        I = self.incenter(A, B, C)
        return self.second_meet_pp_c(A, I, O)

    def amidp_same(self, B, C, A):
        M = self.amidp_opp(B, C, A)
        O = self.circumcenter(A, B, C)
        return self.second_meet_pp_c(M, O, O)

    #####################
    ## Utilities
    ####################

    def line2twoPts(pred, ps):
        if pred == "connecting":
            return self.lookup_pts(ps)
        elif pred == "paraAt":
            X, A, B = self.lookup_pts(ps)
            return X, X + B - A
        elif pred == "perpAt":
            X, A, B = self.lookup_pts(ps)
            return X, X + self.rotate_counterclockwise_90(A - B)
        elif pred == "mediator":
            A, B = self.lookup_pts(ps)
            M = self.midp(A, B)
            return M, M + self.rotate_counterclockwise_90(A - B)
        elif pred == "ibisector":
            A, B, C = self.lookup_pts(ps)
            # X = B + (A - B).smul(self.divV(self.dist(B, C), self.dist(B, A)))
            X = B + (A - B).smul(self.dist(B, C) / self.dist(B, A))
            M = self.midp(X, C)
            return B, M
        elif pred == "ebisector":
            A, B, C = self.lookup_pts(ps)
            X = B + (A - B).smul(self.dist(B, C) / self.dist(B, A))
            # X = B + (A - B).smul(self.divV(self.dist(B, C), self.dist(B, A)))
            M = self.midp(X, C)
            Y = B + self.rotate_counterclockwise_90(M - B)
            return B, Y
        elif pred == "eqoangle":
            B, C, D, E, F = self.lookup_pts(ps)
            theta = self.angle(D, E, F)
            X = B + self.rotate_counterclockwise(theta, C - B)
            return B, X
        else: raise RuntimeException(f"[line2nf] Unexpected line pred: {pred}")

    def line2sif(self, l):
        p1, p2 = self.line2twoPts(l.pred, l.points)
        return self.pp2sif(p1, p2)

    # Two points on a line to slope-intercept form (y = mx + b)
    def pp2sif(self, p1, p2):
        (x1, y1) = p1
        (x2, y2) = p2

        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        return SlopeInterceptForm(m=m, b=b, p1=p1, p2=p2)

    def circ2nf(self, circ):
        pred = circ.pred
        ps = circ.points

        if pred == "c3":
            A, B, C = self.lookup_pts(ps)
            O = self.circumcenter(A, B, C)
            return CircleNF(center=O, radius=self.dist(O, A))
        elif pred == "cOA":
            O, A = self.lookup_pts(ps)
            return CircleNF(center=O, radius=self.dist(O, A))
        elif pred == "cong":
            O, X, Y = self.lookup_pts(ps)
            return CircleNF(center=O, radius=self.dist(X, Y))
        elif pred == "diam":
            B, C = self.lookup_pts(ps)
            O = self.midp(B, C)
            return CircleNF(center=O, radius=dist(O, B))
        else:
            raise RuntimeError(f"[circ2nf] NYI: {pred}")

    def shift(self, O, Ps):
        return [self.get_point(P.x - O.x, P.y - O.y) for P in Ps]

    def unshift(O, Ps):
        return [self.get_point(P.x + O.x, P.y + O.y) for P in Ps]

    def pt_eq(self, p1, p2):
        return self.less(self.dist(p1, p2), 1e-6)

    def pt_neq(self, p1, p2):
        return self.greater(self.dist(p1, p2), 1e-6)

    def process_rs(self, P1, P2, root_select):
        pred = root_select.pred
        rs_args = root_select.vars
        if pred == "neq":
            [pt] = self.lookup_pts(rs_args)
            return self.cond(self.pt_neq(P1, pt), P1, P2)
        elif pred == "closerTo":
            [pt] = self.lookup_pts(rs_args)
            test = self.lte(self.sqdist(P1, pt), self.sqdist(P2, pt))
            return self.cond(test, P1, P2)
        elif pred == "furtherFrom":
            [pt] = self.lookup_pts(rs_args)
            test = self.lt(self.sqdist(P2, pt), self.sqdist(P1, pt))
            return self.cond(test, P1, P2)
        elif pred == "oppSides":
            [pt] = self.lookup_pts(rs_args[0])
            a, b = self.line2twoPts(rs_args[1])
            return self.cond(self.opp_sides(P1, pt, a, b), P1, P2)
        elif pred == "sameSide":
            [pt] = self.lookup_pts(rs_args[0])
            a, b = self.line2twoPts(rs_args[1])
            return self.cond(self.same_side(P1, pt, a, b), P1, P2)
        elif pred == "arbitrary":
            return P2
        else:
            raise NotImplementedError(f"[process_rs] NYI: {pred}")
