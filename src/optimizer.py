from abc import ABC, abstractmethod
import math
import pdb
import collections
import itertools

from instruction import *
from primitives import Line, Point, Circle, Num
from util import is_number, FuncInfo


# Also stores the points used to compute it
LineSF = collections.namedtuple("LineSF", ["a", "b", "c", "p1", "p2"])

CircleNF = collections.namedtuple("CircleNF", ["center", "radius"])

class Optimizer(ABC):
    def __init__(self, instructions, opts):

        self.name2pt = dict()
        self.name2line = dict()
        self.name2circ = dict()

        self.no_plot_pts = list()

        self.losses = dict()
        self.has_loss = False
        self.opts = opts
        self.instructions = instructions
        self.ndgs = dict()
        self.goals = dict()

        self.circles = list()
        self.segments = list()

        super().__init__()

        # self.preprocess()

    def preprocess(self):
        for i in self.instructions:
            self.process_instruction(i)

    def process_instruction(self, i):

        '''
        for p_name, p_val in self.name2pt.items():
            if not p_val.x.is_real or not p_val.y.is_real:
                pdb.set_trace()
        pdb.set_trace()
        '''

        if isinstance(i, Sample):
            self.sample(i)
        elif isinstance(i, Compute):
            self.compute(i)
        elif isinstance(i, Parameterize):
            self.parameterize(i)
        elif isinstance(i, Assert):
            self.add(i)
        elif isinstance(i, AssertNDG):
            self.addNDG(i)
        elif isinstance(i, Confirm):
            self.confirm(i)
        else:
            raise NotImplementedError("FIXME: Finish process_instruction")

    @abstractmethod
    def get_point(self, x, y):
        pass

    @abstractmethod
    def simplify(self, p, method="all"):
        pass

    def lookup_pt(self, p, name=None):
        if isinstance(p.val, str): # Base case
            return self.name2pt[p]

        if isinstance(p.val, FuncInfo):
            head, args = p.val
            if head == "midp": return self.midp(*self.lookup_pts(args))
            elif head == "circumcenter": return self.circumcenter(*self.lookup_pts(args))
            elif head == "orthocenter": return self.orthocenter(*self.lookup_pts(args))
            elif head == "incenter": return self.incenter(*self.lookup_pts(args))
            elif head == "centroid": return self.centroid(*self.lookup_pts(args))
            elif head == "amidpOpp": return self.amidp_opp(*self.lookup_pts(args))
            elif head == "amidpSame": return self.amidp_same(*self.lookup_pts(args))
            elif head == "excenter": return self.excenter(*self.lookup_pts(args))
            elif head == "harmonicLConj": return self.harmonic_l_conj(*self.lookup_pts(args))
            elif head == "interLL":
                l1, l2 = args
                sf1 = self.line2sf(l1)
                sf2 = self.line2sf(l2)
                return self.inter_ll(sf1, sf2)
            elif head == "interLC":
                l, c, root_select = args
                l_sf = self.line2sf(l)
                cnf = self.circ2nf(c)
                if name:
                    self.make_lc_intersect(name, l_sf, cnf)
                else:
                    # Use random name as point is unnamed, but we still want to force LC to intersect
                    rand_name = get_random_string(6)
                    self.make_lc_intersect(rand_name, l_sf, cnf)
                return self.inter_lc(l_sf, cnf, root_select)
            elif head == "interCC":
                c1, c2, root_select = args
                cnf1 = self.circ2nf(c1)
                cnf2 = self.circ2nf(c2)
                if name:
                    self.make_lc_intersect(name, self.radical_axis(cnf1, cnf2), cnf1)
                else:
                    # Use random name as point is unnamed, but we still want to force LC to intersect
                    rand_name = get_random_string(6)
                    self.make_lc_intersect(rand_name, self.radical_axis(cnf1, cnf2), cnf1)
                return self.inter_cc(cnf1, cnf2, root_select)
            elif head == "isogonal": return self.isogonal(*self.lookup_pts(args))
            elif head == "isotomic": return self.isotomic(*self.lookup_pts(args))
            elif head == "inverse": return self.inverse(*self.lookup_pts(args))
            elif head == "midpFrom": return self.midp_from(*self.lookup_pts(args))
            elif head == "mixtilinearIncenter": return self.mixtilinear_incenter(*self.lookup_pts(args))

            else:
                raise NotImplementedError(f"[lookup_pt] Unsupported head {head}")
        else:
            raise RuntimeError("Invalid point type")

    def lookup_pts(self, ps):
        p_vals = list()
        for p in ps:
            p_vals.append(self.lookup_pt(p))
        return p_vals

    def eval_num(self, n_info):
        n_val = n_info.val
        if not isinstance(n_val, tuple) and is_number(n_val):
            return self.const(n_val)

        n_pred = n_val[0]
        n_args = n_val[1]

        if n_pred == "dist":
            p1, p2 = self.lookup_pts(n_args)
            return self.dist(p1, p2)
        elif n_pred == "uangle":
            p1, p2, p3 = self.lookup_pts(n_args)
            return self.angle(p1, p2, p3)
        elif n_pred == "div":
            n1, n2 = [self.eval_num(n) for n in n_args]
            return n1 / n2
        else:
            raise NotImplementedError(f"[eval_num] Unsupported pred {n_pred}")

    @abstractmethod
    def mkvar(self, name, shape=[], lo=-1.0, hi=1.0, trainable=None):
        pass

    @abstractmethod
    def register_pt(self, p, P):
        pass

    @abstractmethod
    def register_line(self, l, L):
        pass

    @abstractmethod
    def register_circ(self, c, C):
        pass

    @abstractmethod
    def register_loss(self, key, var, weight=1.0):
        pass

    @abstractmethod
    def register_ndg(self, key, var, weight=1.0):
        pass

    @abstractmethod
    def register_goal(self, key, var):
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
    def cond(self, cond, t_lam, f_lam):
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
    def eq(self, x, y):
        pass

    @abstractmethod
    def logical_or(self, x, y):
        pass

    @abstractmethod
    def abs(self, x):
        pass

    @abstractmethod
    def exp(self, x):
        pass

    def softmax(self, xs):
        exps = [self.exp(x) for x in xs]
        sum_exps = self.sum(exps)
        return [e / sum_exps for e in exps]

    #####################
    ## Sample
    ####################

    def sample(self, i):
        s_method = i.sampler
        s_args = i.args
        if s_method == "acuteIsoTri": self.sample_triangle(i.points, iso=s_args[0], acute=True)
        elif s_method == "acuteTri": self.sample_triangle(i.points, acute=True)
        elif s_method == "equiTri": self.sample_triangle(i.points, equi=True)
        elif s_method == "isoTri": self.sample_triangle(i.points, iso=s_args[0])
        elif s_method == "polygon": self.sample_polygon(i.points)
        elif s_method == "rightTri": self.sample_triangle(i.points, right=s_args[0])
        elif s_method == "triangle": self.sample_triangle(i.points)
        else: raise NotImplementedError(f"[sample] NYI: Sampling method {s_method}")

    def sample_uniform(self, p):
        P   = self.get_point(x=self.mkvar(str(p)+"x"), y=self.mkvar(str(p)+"y"))
        self.register_pt(p, P)
        return P


    def sample_polygon(self, ps):
        if len(ps) < 4:
            print("WARNING: sample_polygon expecting >3 points")

        angle_zs = [self.mkvar(name=f"polygon_angle_zs_{i}") for i in range(len(ps))]
        multiplicand = ((len(ps) - 2) / len(ps)) * math.pi
        angles = [multiplicand + (math.pi / 3) * self.tanh(0.2 * az) for az in angle_zs]

        scale_zs = [self.mkvar(name=f"polygon_scale_zs_{i}") for i in range(len(ps))]
        scales = [0.5 * self.tanh(0.2 * sz) for sz in scale_zs]

        Ps = [self.get_point(self.const(-2.0), self.const(0.0)),
              self.get_point(self.const(2.0), self.const(0.0))]
        s = self.dist(Ps[0], Ps[1])

        for i in range(2, len(ps) + 1):
            # print(f"sampling polygon point: {i}")
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

        for i in range(len(ps)):
            self.segments.append((Ps[i], Ps[(i+1) % (len(ps))]))

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

        self.segments.extend([(A, B), (B, C), (C, A)])

    #####################
    ## Compute
    ####################

    def compute(self, i):
        obj_name = i.obj_name
        c_method = i.computation.val[0]
        c_args = i.computation.val
        if isinstance(i.computation, Point):
            P = self.lookup_pt(i.computation, str(obj_name))
            self.register_pt(obj_name, P)

            # Add drawings
            if c_method == "midp":
                A, B = self.lookup_pts(c_args[1])
                self.segments.append((A, B))
            elif c_method == "midpFrom":
                M, A = self.lookup_pts(c_args[1])
                self.segments.append((P, A))
            elif c_method == "circumcenter":
                A, _, _ = self.lookup_pts(c_args[1])
                self.circles.append((P, self.dist(P, A))) # P is the circumcenter
            elif c_method == "incenter":
                A, B, C = self.lookup_pts(c_args[1])
                self.circles.append((P, self.inradius(A, B, C))) # P is the incenter
            elif c_method == "excenter":
                A, B, C = self.lookup_pts(c_args[1])
                self.circles.append((P, self.exradius(A, B, C))) # P is the excenter
            elif c_method == "mixtilinearIncenter":
                A, B, C = self.lookup_pts(c_args[1])
                self.circles.append((P, self.mixtilinear_inradius(A, B, C))) # P is the mixtilinearIncenter
            elif c_method == "inverse":
                X, O, A = self.lookup_pts(c_args[1])
                self.circles.append((O, self.dist(O, A)))
            elif c_method == "harmonicLConj":
                X, A, B = self.lookup_pts(ps)
                self.segments.append((A, B))
                self.segments.append((X, P))
        elif isinstance(i.computation, Line):
            L = self.line2sf(i.computation)
            self.register_line(obj_name, L)
        elif isinstance(i.computation, Circle):
            C = self.circ2nf(i.computation)
            self.register_circ(obj_name, C)
        else:
            raise NotImplementedError(f"[compute] NYI: {c_method} not supported")

    def compute_midp(self, m, ps):
        A, B = self.lookup_pts(ps)
        M = self.midp(A, B)
        self.register_pt(m, M)
        self.segments.append((A, B))

    def compute_midp_from(self, p, ps):
        M, A = self.lookup_pts(ps)
        P = self.midp_from(M, A)
        self.register_pt(p, P)
        self.segments.append((P, A))

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
        self.circles.append((O, self.dist(O, A)))

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
        self.circles.append((I, self.inradius(A, B, C)))

    def compute_excenter(self, i, ps):
        A, B, C = self.lookup_pts(ps)
        I = self.excenter(A, B, C)
        self.register_pt(i, I)
        self.circles.append((I, self.exradius(A, B, C)))

    def compute_inter_ll(self, p, l1, l2):
        sf1 = self.line2sf(l1)
        sf2 = self.line2sf(l2)
        P = self.inter_ll(sf1, sf2)
        self.register_pt(p, P)

    def compute_inter_lc(self, p, l, c, root_select):
        l_sf = self.line2sf(l)
        cnf = self.circ2nf(c)
        P = self.inter_lc(l_sf, cnf, root_select)
        self.make_lc_intersect(p, l_sf, cnf)
        self.register_pt(p, P)

    def compute_inter_cc(self, p, c1, c2, root_select):
        cnf1 = self.circ2nf(c1)
        cnf2 = self.circ2nf(c2)
        P = self.inter_cc(cnf1, cnf2, root_select)
        self.make_lc_intersect(p, self.radical_axis(cnf1, cnf2), cnf1)
        self.register_pt(p, P)

    def compute_mixtilinear_incenter(self, i, ps):
        A, B, C = self.lookup_pts(ps)
        I = self.mixtilinear_incenter(A, B, C)
        self.register_pt(i, I)
        self.circles.append((I, self.mixtilinear_inradius(A, B, C)))


    def compute_isogonal(self, y, ps):
        X, A, B, C = self.lookup_pts(ps)
        Y = self.isogonal(X, A, B, C)
        self.register_pt(y, Y)

    def compute_isotomic(self, y, ps):
        X, A, B, C = self.lookup_pts(ps)
        Y = self.isotomic(X, A, B, C)
        self.register_pt(y, Y)

    def compute_inverse(self, y, ps):
        X, O, A = self.lookup_pts(ps)
        Y = self.inverse(X, O, A)
        self.register_pt(y, Y)
        self.circles.append((O, self.dist(O, A)))

    def compute_harmonic_l_conj(self, y, ps):
        X, A, B = self.lookup_pts(ps)
        Y = self.harmonic_l_conj(X, A, B)
        self.register_pt(y, Y)
        self.segments.append((A, B))
        self.segments.append((X, Y))

    #####################
    ## Parameterize
    ####################

    def parameterize(self, i):
        p_name = i.obj_name
        p_method = i.parameterization[0]
        p_args = i.parameterization
        param_method = i.parameterization
        if p_method == "coords": self.parameterize_coords(p_name)
        elif p_method == "inPoly": self.parameterize_in_poly(p_name, p_args[1])
        elif p_method == "onCirc": self.parameterize_on_circ(p_name, p_args[1])
        elif p_method == "onLine": self.parameterize_on_line(p_name, p_args[1])
        elif p_method == "onRay": self.parameterize_on_ray(p_name, p_args[1])
        elif p_method == "onRayOpp": self.parameterize_on_ray_opp(p_name, p_args[1])
        elif p_method == "onSeg": self.parameterize_on_seg(p_name, p_args[1])
        elif p_method == "line": self.parameterize_line(p_name)
        elif p_method == "circle": self.parameterize_circ(p_name)
        else: raise NotImplementedError(f"FIXME: Finish parameterize: {i}")

    def parameterize_coords(self, p):
        self.sample_uniform(p)

    def parameterize_line(self, l):
        p1 = Point(l.val + "_p1")
        p2 = Point(l.val + "_p2")
        self.no_plot_pts += [p1, p2]

        P1 = self.sample_uniform(p1)
        P2 = self.sample_uniform(p2)

        self.register_line(l, self.pp2sf(P1, P2))

    def parameterize_circ(self, c):
        o = Point(c.val + "_origin")
        O = self.sample_uniform(o)
        self.no_plot_pts.append(o)
        circ_nf = CircleNF(center=O, radius=self.mkvar(name=f"{c.val}_origin", lo=0.25, hi=3.0))
        self.register_circ(c, circ_nf)

    def parameterize_on_seg(self, p, ps):
        A, B = self.lookup_pts(ps)
        z = self.mkvar(name=f"{p}_seg")
        z = 0.2 * z
        self.register_loss(f"{p}_seg_regularization", z, weight=1e-4)
        self.register_pt(p, A + (B - A).smul(self.sigmoid(z)))
        self.segments.append((A, B))

    def parameterize_on_line(self, p, p_args):
        [l] = p_args
        A, B = self.line2twoPts(l)
        z = self.mkvar(name=f"{p}_line")
        z = 0.2 * z
        self.register_loss(f"{p}_line_regularization", z, weight=1e-4)
        # TODO: arbitrary and awkward. Better to sample "zones" first?
        s = 3.0
        P1 = A + (A - B).smul(s)
        P2 = B + (B - A).smul(s)
        self.register_pt(p, P1 + (P2 - P1).smul(self.sigmoid(z)))
        self.segments.append((A, B))

    def parameterize_on_ray(self, p, ps):
        A, B = self.lookup_pts(ps)
        z = self.mkvar(name=f"{p}_ray")
        P = A + (B - A).smul(self.exp(z))
        self.register_pt(p, P)
        self.segments.extend([(A, B), (A, P)])

    def parameterize_on_ray_opp(self, p, ps):
        A, B = self.lookup_pts(ps)
        z = self.mkvar(f"{p}_ray_opp")
        P = A + (A - B).smul(self.exp(z))
        self.register_pt(p, P)
        self.segments.extend([(A, B), (A, P)])

    def parameterize_on_circ(self, p, p_args):
        [circ] = p_args
        O, r = self.circ2nf(circ)
        rot = self.mkvar(name=f"{p}_rot")
        theta = rot * 2 * self.const(math.pi)
        X = self.get_point(x=O.x + r * self.cos(theta), y=O.y + r * self.sin(theta))
        self.register_pt(p, X)
        self.circles.append((O, r))

    def parameterize_in_poly(self, p, ps):
        Ps = self.lookup_pts(ps)
        zs = [self.mkvar(name=f"{p}_in_poly_{poly_p}") for poly_p in ps]
        ws = self.softmax(zs)
        Px = self.sum([P.x * w for (P, w) in zip(Ps, ws)])
        Py = self.sum([P.y * w for (P, w) in zip(Ps, ws)])
        P = self.get_point(Px, Py)
        self.register_pt(p, P)

    #####################
    ## Assert
    ####################

    def add(self, assertion):
        self.has_loss = True
        cons = assertion.constraint
        pred, args, negate = cons.pred, cons.args, cons.negate

        if negate:
            raise RuntimeError("[add] Mishandled negation")

        vals = self.assertion_vals(pred, args)

        a_str = f"{pred}_{'_'.join([str(a) for a in args])}"
        weight = 1 / len(vals)
        for i, val in enumerate(vals):
            loss_str = a_str if len(vals) == 1 else f"{a_str}_{i}"
            self.register_loss(loss_str, val, weight=weight)

    def addNDG(self, ndg):
        self.has_loss = True
        ndg_cons = ndg.constraint
        pred, args = ndg_cons.pred, ndg_cons.args

        vals = self.assertion_vals(pred, args)

        a_str = f"not_{pred}_{'_'.join([str(a) for a in args])}"
        weight = 1 / len(vals)

        for i, val in enumerate(vals):
            ndg_str = a_str if len(vals) == 1 else f"{a_str}_{i}"
            self.register_ndg(ndg_str, val, weight=weight)

    def confirm(self, goal):
        goal_cons = goal.constraint
        pred, args, negate = goal_cons.pred, goal_cons.args, goal_cons.negate

        vals = self.assertion_vals(pred, args)
        g_str = f"{pred}_{'_'.join([str(a) for a in args])}"
        if negate:
            print("WARNING: Satisfied NDG goals will have non-zero values")
            g_str = f"not_{g_str}"

        for i, val in enumerate(vals):
            goal_str = g_str if len(vals) == 1 else f"{g_str}_{i}"
            self.register_goal(goal_str, val)

    def assertion_vals(self, pred, args):
        if pred == "amidpOpp":
            M, B, C, A = self.lookup_pts(args)
            return [self.dist(M, self.amidp_opp(B, C, A))]
        elif pred == "amidpSame":
            M, B, C, A = self.lookup_pts(args)
            return [self.dist(M, self.amidp_same(B, C, A))]
        elif pred == "between": return self.between_gap(*self.lookup_pts(args))
        elif pred == "circumcenter":
            O, A, B, C = self.lookup_pts(args)
            self.circles.append((O, self.dist(O, A)))
            return [self.dist(O, self.circumcenter(A, B, C))]
        elif pred == "coll":
            coll_args = self.lookup_pts(args)
            diffs = [self.coll_phi(A, B, C) for A, B, C in itertools.combinations(coll_args, 3)]
            for i in range(len(coll_args)-1):
                self.segments.append((coll_args[i], coll_args[i+1]))
            return diffs
        elif pred == "concur":
            l1, l2, l3 = args
            return [self.concur_phi(l1, l2, l3)]
        elif pred == "cong":
            A, B, C, D = self.lookup_pts(args)
            if A in [C, D]: self.circles.append((A, self.dist(A, B)))
            elif B in [C, D]: self.circles.append((B, self.dist(A, B)))
            return [self.cong_diff(A, B, C, D)]
        elif pred == "contri":
            [A, B, C, P, Q, R] = self.lookup_pts(args)
            self.segments.extend([(A, B), (B, C), (C, A), (P, Q), (Q, R), (R, P)])
            return [self.eqangle6_diff(A, B, C, P, Q, R),
                    self.eqangle6_diff(B, C, A, Q, R, P),
                    self.eqangle6_diff(C, A, B, R, P, Q),
                    self.cong_diff(A, B, P, Q),
                    self.cong_diff(A, C, P, R),
                    self.cong_diff(B, C, Q, R)]
        elif pred == "cycl":
            cycl_args = self.lookup_pts(args)
            assert(len(cycl_args) > 3)
            O = self.circumcenter(*cycl_args[:3])
            diffs = list()
            diffs = [self.eqangle6_diff(A, B, D, A, C, D) for A, B, C, D in itertools.combinations(cycl_args, 4)]
            self.circles.append((O, self.dist(O, cycl_args[0])))
            return diffs
        elif pred == "distLt":
            X, Y, A, B = self.lookup_pts(args)
            return [self.max(self.const(0.0), self.dist(X, Y) - dist(A, B))]
        elif pred == "distGt":
            X, Y, A, B = self.lookup_pts(args)
            return [self.max(self.const(0.0), self.dist(A, B) - self.dist(X, Y))]
        elif pred == "eq":
            n1, n2 = [self.eval_num(n) for n in args]
            return [n1 - n2]
        elif pred == "eqangle": return [self.eqangle8_diff(*self.lookup_pts(args))]
        elif pred == "eqoangle":
            A, B, C, P, Q, R = self.lookup_pts(args)
            return [self.angle(A, B, C) - self.angle(P, Q, R)]
        elif pred == "eqratio": return [self.eqratio_diff(*self.lookup_pts(args))]
        elif pred == "foot":
            F, X, A, B = self.lookup_pts(args)
            return [self.coll_phi(F, A, B), self.perp_phi(F, X, A, B)]
        elif pred == "ibisector":
            X, B, A, C = self.lookup_pts(args)
            self.segments.extend([(B, A), (A, X), (A, C)])
            return [self.eqangle8_diff(B, A, A, X, X, A, A, C)]
        elif pred == "incenter":
            I, A, B, C = self.lookup_pts(args)
            return [self.dist(I, self.incenter(A, B, C))]
        elif pred == "insidePolygon": return self.in_poly_phis(*self.lookup_pts(args))
        elif pred == "interLL":
            X, A, B, C, D = self.lookup_pts(args)
            return [self.coll_phi(X, A, B), self.coll_phi(X, C, D)]
        elif pred == "isogonal":
            X, Y, A, B, C = self.lookup_pts(args)
            return [self.dist(X, self.isogonal(Y, A, B, C))]
        elif pred == "midp":
            M, A, B = self.lookup_pts(args)
            return [self.dist(M, self.midp(A, B))]
        elif pred == "onCirc":
            X, C = args
            [X] = self.lookup_pts([X])
            (O, r) = self.circ2nf(C)
            return [self.dist(O, X) - r]
        elif pred == "onLine":
            [X, l] = args
            [X] = self.lookup_pts([X])
            lp1, lp2 = self.line2twoPts(l)
            return [self.coll_phi(X, lp1, lp2)]
        elif pred == "onRay": return [self.coll_phi(*self.lookup_pts(args))] + self.onray_gap(*self.lookup_pts(args))
        elif pred == "onSeg": return [self.coll_phi(*self.lookup_pts(args))] + self.between_gap(*self.lookup_pts(args))
        elif pred == "oppSides":
            A, B, X, Y = self.lookup_pts(args)
            return [self.max(self.const(0.0), self.side_score_prod(A, B, X, Y))]
        elif pred == "orthocenter":
            H, A, B, C = self.lookup_pts(args)
            return [self.dist(H, self.orthocenter(A, B, C))]
        elif pred == "perp": return [self.perp_phi(*self.lookup_pts(args))]
        elif pred == "para":
            if len(args) == 4: # four points
                return [self.para_phi(*self.lookup_pts(args))]
            else: # two lines
                raise NotImplementedError("Fix now that we are using standard form")
                '''
                l1, l2 = args
                m1, b1, _, _ = self.line2sif(l1)
                m2, b2, _, _ = self.line2sif(l2)
                return [m2 - m1]
                '''
        elif pred == "reflectPL":
            X, Y, A, B = self.lookup_pts(args)
            return [self.perp_phi(X, Y, A, B), self.cong_diff(A, X, A, Y)]
        elif pred == "sameSide":
            A, B, X, Y = self.lookup_pts(args)
            return [self.max(self.const(0.0), -self.side_score_prod(A, B, X, Y))]
        elif pred == "simtri":
            [A, B, C, P, Q, R] = self.lookup_pts(args)
            self.segments.extend([(A, B), (B, C), (C, A), (P, Q), (Q, R), (R, P)])
            # this is *too* easy to optimize, eqangle properties don't end up holding
            # return [eqratio_diff(A, B, B, C, P, Q, Q, R), eqratio_diff(B, C, C, A, Q, R, R, P), eqratio_diff(C, A, A, B, R, P, P, Q)]
            return [self.eqangle6_diff(A, B, C, P, Q, R), self.eqangle6_diff(B, C, A, Q, R, P), self.eqangle6_diff(C, A, B, R, P, Q)]
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

    def scalar_product(self, A, O, B):
        lhs = (A.x - O.x) * (B.x - O.x)
        rhs = (A.y - O.y) * (B.y - O.y)
        return lhs + rhs

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

    def concur_phi(self, l1, l2, l3):
        a1, b1, c1, _, _ = self.line2sf(l1)
        a2, b2, c2, _, _ = self.line2sf(l2)
        a3, b3, c3, _, _ = self.line2sf(l3)

        # [[a, b], [c, d]]
        def det2x2(a, b, c, d):
            return a * d - c * b

        # [[a, b, c], [d, e, f], [g, h, i]]
        def det3x3(a, b, c, d, e, f, g, h, i):
            return a * det2x2(e, f, h, i) - b * det2x2(d, f, g, i) + c * det2x2(d, e, g, h)

        return det3x3(a1, b1, c1, a2, b2, c2, a3, b3, c3)


    def between_gap(self, X, A, B):
        eps = 0.2

        A1 = self.get_point(A.x + eps * (B.x - A.x), A.y + eps * (B.y - A.y))
        B1 = self.get_point(B.x + eps * (A.x - B.x), B.y + eps * (A.y - B.y))

        return [self.diff_signs(X.x - A1.x, X.x - B1.x), self.diff_signs(X.y - A1.y, X.y - B1.y)]

    def onray_gap(self, X, A, B):
        eps = 0.2
        A1 = self.get_point(A.x + eps * (B.x - A.x), A.y + eps * (B.y - A.y))

        # TODO: coll_phi causing NaNs when [X, A, B] are perfectly collinear by construction
        return [self.diff_signs(X.x - A1.x, A1.x - B.x), self.diff_signs(X.y - A1.y, A1.y - B.y)]

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

    def inter_ll(self, sf1, sf2):
        (a1, b1, c1, _, _) = sf1
        (a2, b2, c2, _, _) = sf2

        def intersect_vert_l1_with_l2():
            const_x = c1
            py = (c2 - a2 * const_x) / b2 # will fail if line 2 is vertical as well (b2 == 0)
            return self.get_point(const_x, py)

        def intersect_vert_l2_with_l1():
            const_x = c2
            py = (c1 - a1 * const_x) / b1 # will fail if line 1 is vertical as well (b1 == 0)
            return self.get_point(const_x, py)

        def intersect_non_vert_lines():
            # ax + by = c --> y = (-ax + c) / b --> y = (-a / b)x + (c / b)
            m1, int1 = (-a1 / b1), (c1 / b1)
            m2, int2 = (-a2 / b2), (c2 / b2)
            # If both lines are horizontal, denominator will be 0
            px = (int2 - int1) / (m1 - m2)
            py = m1 * px + int1
            return self.get_point(px, py)

        return self.cond(self.eq(b1, self.const(0)), # sf1 is vertical
                         intersect_vert_l1_with_l2,
                         lambda: self.cond(self.eq(b2, self.const(0)), # sf2 is vertical
                                           intersect_vert_l2_with_l1,
                                           intersect_non_vert_lines))


    def inter_pp_c(self, P1, P2, cnf):
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
                return self.cond(self.lt(x, self.const(0.0)), lambda: self.const(-1.0), lambda: self.const(1.0))

            # NEXT: Change to self....
            Q1 = self.get_point((D * dy + sgnstar(dy) * dx * self.sqrt(radicand)) / (dr**2),
                                (-D * dx + self.abs(dy) * self.sqrt(radicand)) / (dr**2))

            Q2 = self.get_point((D * dy - sgnstar(dy) * dx * self.sqrt(radicand)) / (dr**2),
                                (-D * dx - self.abs(dy) * self.sqrt(radicand)) / (dr**2))
            return self.unshift(O, [Q1, Q2])

        def on_neg():
            Operp = self.rotate_counterclockwise_90(P1 - P2) + O
            F = self.inter_ll(self.pp2sf(P1, P2), self.pp2sf(O, Operp))
            X = O + (F - O).smul(r / self.dist(O, F))
            Q = self.midp(F, X)
            return self.unshift(O, [Q, Q])

        return self.cond(self.lt(radicand, self.const(0.0)), on_neg, on_nneg)

    def inter_lc(self, l, c, root_select):
        p1, p2 = l.p1, l.p2
        I1, I2 = self.inter_pp_c(p1, p2, c)
        self.circles.append(c)
        return self.process_rs(I1, I2, root_select)

    def inter_cc(self, cnf1, cnf2, root_select):
        l = self.radical_axis(cnf1, cnf2)
        result = self.inter_lc(l, cnf1, root_select)
        self.circles.append(cnf1)
        self.circles.append(cnf2)
        return result

    def make_lc_intersect(self, name, l, c):
        _, _, _, A, B = l
        O, r = c
        Operp = self.rotate_counterclockwise_90(A - B) + O

        F = self.inter_ll(l, self.pp2sf(O, Operp))
        d = self.dist(O, F)
        f_val = self.cond(self.lt(r, d), lambda: d, lambda: self.const(0.0))

        loss = self.cond(self.logical_or(self.lt(self.dist(O, Operp), 1e-6),
                                         self.lt(self.dist(A, B), 1e-6)),
                         lambda: self.const(0.0), lambda: f_val)
        self.register_loss(f"interLC_{name}", loss, weight=1e-1)

    def second_meet_pp_c(self, A, B, O):
        P1, P2 = self.inter_pp_c(A, B, CircleNF(O, self.dist(O, A)))
        return self.cond(self.lt(self.sqdist(A, P1), self.sqdist(A, P2)), lambda: P2, lambda: P1)

    def amidp_opp(self, B, C, A):
        O = self.circumcenter(A, B, C)
        I = self.incenter(A, B, C)
        return self.second_meet_pp_c(A, I, O)

    def amidp_same(self, B, C, A):
        M = self.amidp_opp(B, C, A)
        O = self.circumcenter(A, B, C)
        return self.second_meet_pp_c(M, O, O)


    def radical_axis_pts(self, cnf1, cnf2):
        (c1x, c1y), r1 = cnf1
        (c2x, c2y), r2 = cnf2

        A = self.const(2.0) * (c2x - c1x)
        B = self.const(2.0) * (c2y - c1y)
        C = (r1**2 - r2**2) + (c2y**2 - c1y**2) + (c2x**2 - c1x**2)

        # FIXME: Fails on EGMO 2.7 because we aren't passing around lambdas anymore
        # pdb.set_trace()
        test = self.gt(self.abs(A), 1e-6)
        p1 = self.cond(test,
                       lambda: self.get_point(x=(C-B)/A, y=self.const(1.0)),
                       lambda: self.get_point(x=self.const(1.0), y=C/B))
        p2 = self.cond(test,
                       lambda: self.get_point(x=C/A, y=self.const(0.0)),
                       lambda: self.get_point(x=self.const(0.0), y=C/B))

        return p1, p2

    def radical_axis(self, cnf1, cnf2):
        p1, p2 = self.radical_axis_pts(cnf1, cnf2)
        return self.pp2sf(p1, p2)

    def eqangle6_diff(self, A, B, C, P, Q, R):
        s1 = self.det3(A, B, C)
        c1 = self.scalar_product(A, B, C)
        s2 = self.det3(P, Q, R)
        c2 = self.scalar_product(P, Q, R)
        return 0.1 * (s1 * c2 - s2 * c1)

    def eqratio_diff(self, A, B, C, D, P, Q, R, S):
        # AB/CD = PQ/RS
        return self.sqrt(dist(A, B) * self.dist(R, S)) - self.sqrt(self.dist(P, Q) * self.dist(C, D))

    def cycl_diff(self, A, B, C, D):
        return self.eqangle6_diff(A, B, D, A, C, D)

    def eqangle8_diff(self, A, B1, B2, C, P, Q1, Q2, R):
        return self.eqangle6_diff(A, B1, C - B2 + B1, P, Q1, R - Q2 + Q1)

    def semiperimeter(self, A, B, C):
        a, b, c = self.side_lengths(A, B, C)
        return (a + b + c) / 2

    def area(self, A, B, C):
        a, b, c = self.side_lengths(A, B, C)
        s = self.semiperimeter(A, B, C)
        return self.sqrt(s * (s - a) * (s - b) * (s - c))

    def inradius(self, A, B, C):
        return self.area(A, B, C) / self.semiperimeter(A, B, C)

    def exradius(self, A, B, C):
        r = self.inradius(A, B, C)
        a, b, c = self.side_lengths(A, B, C)
        s = (a + b + c)/2
        return r * s / (s - a)

    def mixtilinear_incenter(self, A, B, C):
        ta, tb, tc = self.angle(C, A, B), self.angle(A, B, C), self.angle(B, C, A)
        return self.trilinear(A, B, C, (1/2) * (1 + self.cos(ta) - self.cos(tb) - self.cos(tc)), 1, 1)

    def mixtilinear_inradius(self, A, B, C):
        r = self.inradius(A, B, C)
        ta = self.angle(C, A, B)
        return r * (1 / self.cos(ta / 2)**2)


    def to_trilinear(self, P, A, B, C):
        la = self.pp2sf(B, C)
        lb = self.pp2sf(C, A)
        lc = self.pp2sf(A, B)

        ga = self.pp2sf(P, P + self.rotate_counterclockwise_90(C - B))
        gb = self.pp2sf(P, P + self.rotate_counterclockwise_90(A - C))
        gc = self.pp2sf(P, P + self.rotate_counterclockwise_90(B - A))

        da = self.dist(P, self.inter_ll(la, ga))
        db = self.dist(P, self.inter_ll(lb, gb))
        dc = self.dist(P, self.inter_ll(lc, gc))

        da = self.cond(self.opp_sides(P, A, B, C), lambda: -da, lambda: da)
        db = self.cond(self.opp_sides(P, B, C, A), lambda: -db, lambda: db)
        dc = self.cond(self.opp_sides(P, C, A, B), lambda: -dc, lambda: dc)
        return da, db, dc

    def invert_or_zero(self, x):
        return self.cond(self.abs(x) < 1e-5, lambda: self.const(0.0), lambda: self.const(1) / x)

    def isogonal(self, P, A, B, C):
        x, y, z = self.to_trilinear(P, A, B, C)
        return self.trilinear(A, B, C, self.invert_or_zero(x), self.invert_or_zero(y), self.invert_or_zero(z))

    def isotomic(self, P, A, B, C):
        a, b, c = self.side_lengths(A, B, C)
        x, y, z = self.to_trilinear(P, A, B, C)
        return self.trilinear(A, B, C, (a**2) * self.invert_or_zero(x), (b**2) * self.invert_or_zero(y), (c**2) * self.invert_or_zero(z))


    def inverse(self, X, O, A):
        return O + (X - O).smul(self.sqdist(O, A) / self.sqdist(O, X))

    def harmonic_l_conj(self, X, A, B):
        # see picture in https://en.wikipedia.org/wiki/Projective_harmonic_conjugate
        # L is arbitrary here, not on the line X A B
        # (could also do case analysis and cross-ratio)
        L = A + self.rotate_counterclockwise(const(math.pi / 3), X - A).smul(0.5)
        M = self.midp(A, L)
        N = self.inter_ll(self.pp2sf(B, L), self.pp2sf(X, M))
        K = self.inter_ll(self.pp2sf(A, N), self.pp2sf(B, M))
        Y = self.inter_ll(self.pp2sf(L, K), self.pp2sf(A, X))
        return Y

    def in_poly_phis(self, X, *Ps):
        phis = []
        n = len(Ps)
        for i in range(n):
            A, B, C = Ps[i], Ps[(i+1) % n], Ps[(i+2) % n]
            # X and C are on the same side of AB
            phis.append(self.max(self.const(0.0), - self.side_score_prod(X, C, A, B)))
        return phis

    #####################
    ## Utilities
    ####################

    def line2twoPts(self, l):
        if isinstance(l.val, str):
            L = self.name2line[l]
            return L.p1, L.p2
        elif isinstance(l.val, FuncInfo):
            pred, args = l.val
            if pred == "connecting":
                return self.lookup_pts(args)
            elif pred == "paraAt":
                X, A, B = self.lookup_pts(args)
                return X, X + B - A
            elif pred == "perpAt":
                X, A, B = self.lookup_pts(args)
                return X, X + self.rotate_counterclockwise_90(A - B)
            elif pred == "perpBis":
                a, b = args
                m_ab = Point(("midp", [a, b]))
                return self.line2twoPts(Line(FuncInfo("perpAt", [m_ab, a, b])))
            elif pred == "mediator":
                A, B = self.lookup_pts(args)
                M = self.midp(A, B)
                return M, M + self.rotate_counterclockwise_90(A - B)
            elif pred == "ibisector":
                A, B, C = self.lookup_pts(args)
                X = B + (A - B).smul(self.dist(B, C) / self.dist(B, A))
                M = self.midp(X, C)
                return B, M
            elif pred == "ebisector":
                A, B, C = self.lookup_pts(args)
                X = B + (A - B).smul(self.dist(B, C) / self.dist(B, A))
                M = self.midp(X, C)
                Y = B + self.rotate_counterclockwise_90(M - B)
                return B, Y
            elif pred == "eqoangle":
                B, C, D, E, F = self.lookup_pts(args)
                theta = self.angle(D, E, F)
                X = B + self.rotate_counterclockwise(theta, C - B)
                self.segments.extend([(A, B), (B, C), (P, Q), (Q, R)])
                return B, X
            else:
                raise RuntimeError(f"[line2twoPts] Unexpected line pred: {pred}")
        else:
            raise RuntimeError(f"Unsupported line type: {type(l)}")

    def line2sf(self, l):
        if isinstance(l.val, str):
            return self.name2line[l]
        else:
            p1, p2 = self.line2twoPts(l)
            return self.pp2sf(p1, p2)

    def pp2sf(self, p1, p2):
        def vert_line():
            return LineSF(self.const(1.0), self.const(0.0), p1.x, p1, p2)

        def horiz_line():
            return LineSF(self.const(0.0), self.const(1.0), p1.y, p1, p2)

        def calc_sf_from_slope_intercept():
            (x1, y1) = p1
            (x2, y2) = p2

            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            # y = mx + b ---> -mx + (1)y = b
            return LineSF(-m, self.const(1.0), b, p1, p2)

        return self.cond(self.eq(p1.x, p2.x),
                         vert_line,
                         lambda: self.cond(self.eq(p1.y, p2.y),
                                           horiz_line,
                                           calc_sf_from_slope_intercept))

    def circ2nf(self, circ):

        if isinstance(circ.val, str):
            return self.name2circ[circ]
        elif isinstance(circ.val, FuncInfo):

            pred, args = circ.val

            if pred == "c3" or pred == "circumcircle":
                A, B, C = self.lookup_pts(args)
                O = self.circumcenter(A, B, C)
                return CircleNF(center=O, radius=self.dist(O, A))
            elif pred == "coa":
                O, A = self.lookup_pts(args)
                return CircleNF(center=O, radius=self.dist(O, A))
            elif pred == "cong":
                O, X, Y = self.lookup_pts(args)
                return CircleNF(center=O, radius=self.dist(X, Y))
            elif pred == "diam":
                B, C = self.lookup_pts(args)
                O = self.midp(B, C)
                return CircleNF(center=O, radius=self.dist(O, B))
            elif pred == "incircle":
                A, B, C = self.lookup_pts(args)
                I = self.incenter(A, B, C)
                return CircleNF(center=I, radius=self.inradius(A, B, C))
            elif pred == "excircle":
                A, B, C = self.lookup_pts(args)
                I = self.excenter(A, B, C)
                return CircleNF(center=I, radius=self.exradius(A, B, C))
            elif pred == "mixtilinearIncircle":
                A, B, C = self.lookup_pts(args)
                I = self.mixtilinear_incenter(A, B, C)
                return CircleNF(center=I, radius=self.mixtilinear_inradius(A, B, C))
            else:
                raise RuntimeError(f"[circ2nf] NYI: {pred}")
        else:
            raise RuntimeError("Invalid circle type")

    def shift(self, O, Ps):
        return [self.get_point(P.x - O.x, P.y - O.y) for P in Ps]

    def unshift(self, O, Ps):
        return [self.get_point(P.x + O.x, P.y + O.y) for P in Ps]

    def pt_eq(self, p1, p2):
        return self.lt(self.dist(p1, p2), 1e-6)

    def pt_neq(self, p1, p2):
        return self.gt(self.dist(p1, p2), 1e-6)

    def process_rs(self, P1, P2, root_select):
        pred = root_select.pred
        rs_args = root_select.vars
        if pred == "neq":
            [pt] = self.lookup_pts(rs_args)
            return self.cond(self.pt_neq(P1, pt), lambda: P1, lambda: P2)
        elif pred == "closerTo":
            [pt] = self.lookup_pts(rs_args)
            test = self.lte(self.sqdist(P1, pt), self.sqdist(P2, pt))
            return self.cond(test, lambda: P1, lambda: P2)
        elif pred == "furtherFrom":
            [pt] = self.lookup_pts(rs_args)
            test = self.lt(self.sqdist(P2, pt), self.sqdist(P1, pt))
            return self.cond(test, lambda: P1, lambda: P2)
        elif pred == "oppSides":
            [pt] = self.lookup_pts(rs_args[0])
            a, b = self.line2twoPts(rs_args[1])
            return self.cond(self.opp_sides(P1, pt, a, b), lambda: P1, lambda: P2)
        elif pred == "sameSide":
            [pt] = self.lookup_pts(rs_args[0])
            a, b = self.line2twoPts(rs_args[1])
            return self.cond(self.same_side(P1, pt, a, b), lambda: P1, lambda: P2)
        elif pred == "arbitrary":
            return P2
        else:
            raise NotImplementedError(f"[process_rs] NYI: {pred}")

    def points_far_enough_away(self, name2pt, min_dist):
        for a, b in itertools.combinations(name2pt.keys(), 2):
            A, B = name2pt[a], name2pt[b]
            d = self.dist(A, B)
            if d < min_dist:
                print(f"DUP: {a} {b}")
                return False
        return True

    def diff_signs(self, x, y):
        return self.max(self.const(0.0), x * y)
