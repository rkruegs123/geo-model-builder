import pdb
import copy

from cline import Line, Circle
from instruction import Compute, Parameterize, Assert, AssertNDG
from util import *
from constraint import Constraint

class CompileState:
    def __init__(self, sample_bucket, solve_bucket):

        self.sample_bucket = sample_bucket
        self.solve_bucket = solve_bucket

        self.visited = copy.deepcopy(sample_bucket.points)
        self.solve_instructions = list()
        self.ps = copy.deepcopy(solve_bucket.points)
        self.cs = copy.deepcopy(solve_bucket.assertions)
        self.open_roots = dict()
        self.root_blacklist = list()

        self.compute_tricks = [
            self.computeCircumcenter
            , self.computeMidp
            , self.computeFromMidp
            , self.computeFoot
            , self.computeReflectPL
            , self.computeIncenter
            , self.computeMixIncenter
            , self.computeExcenter
            , self.computeOrthocenter
            , self.computeCentroid
            , self.computeIsogonal
            , self.computeIsotomic
            , self.computeArcMidpOpp
            , self.computeArcMidpSame
            , self.computeInverse
            , self.computeHarmonicLConj
            , self.computeHarmonicCConj
            , self.computeInterLL
            , self.computeInter
        ]

        self.param_tricks = [
            self.paramOnSeg
            , self.paramOnRay
            , self.paramOnLine
            , self.paramOnCirc
            , self.paramInPoly
            , self.paramCoords
        ]

    def solve(self):
        while self.ps:
            p = self.ps.pop(0)
            self.process_point(p)
            self.visited.append(p)

        # Resolve roots
        if self.open_roots:
            for key, root in self.open_roots.items():
                self.root_blacklist.append(root)
            if self.root_blacklist:
                print(f"[WARNING] root blacklist: {self.root_blacklist}")
                self.visited = copy.deepcopy(self.sample_bucket.points)
                self.solve_instructions = list()
                self.ps = copy.deepcopy(self.solve_bucket.points)
                self.cs = copy.deepcopy(self.solve_bucket.assertions)
                self.open_roots = dict()
                self.solve()
        else:
            for c in self.cs:
                self.solve_instructions.append(Assert(c))
                for ordC in c.orders():
                    self.solve_instructions.append(Assert(ordC))
                for ndg in c.ndgs():
                    self.solve_instructions.append(AssertNDG(ndg))


    def process_point(self, p):

        # Get all constraints to process for point p
        cs_for_p = list()
        for c in self.cs:
            if p in c.points and all(p1 == p or p1 in self.visited for p1 in c.points):
                cs_for_p.append(c)

        for trick in (self.compute_tricks + self.param_tricks):
            if trick(p, cs_for_p):
                return

    '''
    Compute Tricks
    '''
    def computeCircumcenter(self, p, cs):
        ccCs = [c for c in cs if c.pred == "circumcenter"]
        for c in ccCs:
            if c.points[0] == p:
                self.solve_instructions.append(Compute(p, ("circumcenter", c.points[1:])))
                self.cs.remove(c)
                return True
        return False

    def computeOrthocenter(self, p, cs):
        orthocenterCs = [c for c in cs if c.pred == "orthocenter"]
        for c in orthocenterCs:
            if c.points[0] == p:
                self.solve_instructions.append(Compute(p, ("orthocenter", c.points[1:])))
                self.cs.remove(c)
                return True
        return False

    def computeCentroid(self, p, cs):
        centroidCs = [c for c in cs if c.pred == "centroid"]
        for c in centroidCs:
            if c.points[0] == p:
                self.solve_instructions.append(Compute(p, ("centroid", c.points[1:])))
                self.cs.remove(c)
                return True
        return False

    def computeIsogonal(self, p, cs):
        isogonalCs = [c for c in cs if c.pred == "isogonal"]
        for c in isogonalCs:
            x, y, a, b, c = c.points
            if x == p:
                self.solve_instructions.append(Compute(p, ("isogonal", [y, a, b, c])))
                self.cs.remove(c)
                return True
            elif y == p:
                self.solve_instructions.append(Compute(p, ("isogonal", [x, a, b, c])))
                self.cs.remove(c)
                return True
        return False

    def computeIsotomic(self, p, cs):
        isotomicCs = [c for c in cs if c.pred == "isotomic"]
        for c in isotomicCs:
            x, y, a, b, c = c.points
            if x == p:
                self.solve_instructions.append(Compute(p, ("isotomic", [y, a, b, c])))
                self.cs.remove(c)
                return True
            elif y == p:
                self.solve_instructions.append(Compute(p, ("isotomic", [x, a, b, c])))
                self.cs.remove(c)
                return True
        return False

    def computeArcMidpOpp(self, p, cs):
        aMidpOppCs = [c for c in cs if c.pred == "arcMidpOpp"]
        for c in aMidpOppCs:
            if c.points[0] == p:
                self.solve_instructions.append(Compute(p, ("arcMidpOpp", c.points[1:])))
                self.cs.remove(c)
                return True
        return False

    def computeArcMidpSame(self, p, cs):
        aMidpSameCs = [c for c in cs if c.pred == "arcMidpSame"]
        for c in aMidpSameCs:
            if c.points[0] == p:
                self.solve_instructions.append(Compute(p, ("arcMidpSame", c.points[1:])))
                self.cs.remove(c)
                return True
        return False

    def computeInverse(self, p, cs):
        # TODO: allow newer point to come second
        inverseCs = [c for c in cs if c.pred == "inverse"]
        for c in inverseCs:
            match_success, match = match_in_first_2(p, c.points)
            if match_success:
                y, o, a = match
                self.solve_instructions.append(Compute(p, ("inverse", [y, o, a])))
                self.cs.remove(c)
                return True
        return False

    def computeHarmonicLConj(self, p, cs):
        harmonicLCs = [c for c in cs if c.pred == "harmonicL"]
        for c in harmonicLCs:
            (y, (a, b)) = group_pairs(p, ps)
            if y is not None:
                self.solve_instructions.append(Compute(p, ("harmonicLConj", [y, a, b])))
                self.cs.remove(c)
                return True
        return False

    def computeHarmonicCConj(self, p, cs):
        harmonicCCs = [c for c in cs if c.pred == "harmonicC"]
        for c in harmonicCCs:
            (y, (a, b)) = group_pairs(p, ps)
            if y is not None:
                self.solve_instructions.append(Compute(p, ("harmonicCConj", [y, a, b])))
                self.cs.remove(c)
                return True
        return False


    def computeMidp(self, p, cs):
        midpCs = [c for c in cs if c.pred == "midp"]
        for c in midpCs:
            if c.points[0] == p:
                self.solve_instructions.append(Compute(p, ("midp", c.points[1:])))
                self.cs.remove(c)
                return True
        return False

    def computeFromMidp(self, p, cs):
        midpCs = [c for c in cs if c.pred == "midp"]
        for c in midpCs:
            m, a, b = c.points
            if m != p:
                x = a
                if a == p:
                    x = b
                self.solve_instructions.append(Compute(p, ("midpFrom", [m, x])))
                self.cs.remove(c)
                return True
        return False

    def computeReflectPL(self, p, cs):
        reflectPLCs = [c for c in cs if c.pred == "reflectPL"]
        for c in reflectPLCs:
            match_success, match = match_in_first_2(p, c.points)
            if match_success:
                x, a, b = match
                self.solve_instructions.append(
                    Compute(p, ("interLC", Line("perpAt", [x, a, b]), Circle("coa", [a, x]), Root("neq", [x])))
                )
                self.cs.remove(c)
                return True
        return False

    def computeFoot(self, p, cs):
        footCs = [c for c in cs if c.pred == "foot"]
        for c in footCs:
            p1, x, a, b = c.points
            if p1 == p:
                self.solve_instructions.append(Compute(p, ("interLL", Line("perpAt", [x, a, b]), Line("connecting", [a, b]))))
                self.cs.remove(c)
                return True
        return False

    def computeIncenter(self, p, cs):
        incenterCs = [c for c in cs if c.pred == "incenter"]
        for c in incenterCs:
            if c.points[0] == p:
                self.solve_instructions.append(Compute(p, ("incenter", c.points[1:])))
                self.cs.remove(c)
                return True
        return False

    def computeMixIncenter(self, p, cs):
        mixIncenterCs = [c for c in cs if c.pred == "mixtilinearIncenter"]
        for c in mixIncenterCs:
            if c.points[0] == p:
                self.solve_instructions.append(Compute(p, ("mixtilinearIncenter", c.points[1:])))
                self.cs.remove(c)
                return True
        return False

    def computeExcenter(self, p, cs):
        excenterCs = [c for c in cs if c.pred == "excenter"]
        for c in excenterCs:
            if c.points[0] == p:
                self.solve_instructions.append(Compute(p, ("excenter", c.points[1:])))
                self.cs.remove(c)
                return True
        return False

    def computeInterLL(self, p, cs):
        interllCs = [c for c in cs if c.pred == "interLL"]
        for c in interllCs:
            if c.points[0] == p:
                w, x, y, z = c.points[1:]
                l1 = Line("connecting", [w, x])
                l2 = Line("connecting", [y, z])
                self.solve_instructions.append(Compute(p, ("interLL", l1, l2)))
                self.cs.remove(c)
                return True
        return False

    def computeInter(self, p, cs):
        lines = self.linesFor(p, cs)
        circles = self.circlesFor(p, cs)

        if len(lines) >= 2:
            cs1, l1, extra_cs1 = lines[0]
            cs2, l2, extra_cs2 = lines[1]
            self.solve_instructions.append(Compute(p, ("interLL", l1, l2)))
            for c in cs1 + cs2:
                self.cs.remove(c)
            self.cs += extra_cs1 + extra_cs2
            return True
        elif len(lines) == 1 and circles:
            cs1, l, extra_cs_l = lines[0]
            cs2, circ, extra_cs_c = circles[0]

            root, rcs = self.determine_root(p, l, circ, cs)
            if root is None:
                return False
            self.solve_instructions.append(Compute(p, ("interLC", l, circ, root)))
            for c in cs1 + cs2 + rcs:
                self.cs.remove(c)
            self.cs += extra_cs_l + extra_cs_c
            return True
        elif len(circles) >= 2:
            cs1, c1, extra_cs1 = circles[0]
            cs2, c2, extra_cs2 = circles[1]

            root, rcs = self.determine_root(p, c1, c2, cs)
            if root is None:
                return False
            self.solve_instructions.append(Compute(p, ("interCC", c1, c2, root)))
            for c in cs1 + cs2 + rcs:
                self.cs.remove(c)
            self.cs += extra_cs1 + extra_cs2
            return True
        return False



    '''
    Parameterization Tricks
    '''
    def paramOnSeg(self, p, cs):
        onSegCs = [c for c in cs if c.pred == "onSeg"]
        for c in onSegCs:
            if c.points[0] == p:
                _, a, b = c.points
                self.solve_instructions.append(Parameterize(p, ("onSeg", [a, b])))
                self.cs.remove(c)
                return True
        return False

    def paramOnRay(self, p, cs):
        onRayCs = [c for c in cs if c.pred == "onRay"]
        for c in onRayCs:
            if c.points[0] == p:
                _, a, b = c.points
                self.solve_instructions.append(Parameterize(p, ("onRay", [a, b])))
                self.cs.remove(c)
                return True
        return False

    def paramInPoly(self, p, cs):
        inPolyCs = [c for c in cs if c.pred == "insidePolygon"]
        for c in inPolyCs:
            if c.points[0] == p:
                self.solve_instructions.append(Parameterize(p, ("inPoly", c.points[1:])))
                self.cs.remove(c)
                return True
        return False

    def paramOnLine(self, p, cs):
        lines = self.linesFor(p, cs)
        if lines:
            lcs, l, extra_cs = lines[0]
            self.solve_instructions.append(Parameterize(p, ("onLine", l)))
            for c in lcs:
                self.cs.remove(c)
            self.cs += extra_cs
            return True
        return False

    def paramOnCirc(self, p, cs):
        circles = self.circlesFor(p, cs)
        if circles:
            ccs, circ, extra_cs = circles[0]
            self.solve_instructions.append(Parameterize(p, ("onCirc", circ)))
            for c in ccs:
                self.cs.remove(c)
            self.cs += extra_cs
            return True
        return False



    def paramCoords(self, p, cs):
        print(f"WARNING: point is parameterized by its coordinates: {p}")
        self.solve_instructions.append(Parameterize(p, ("coords", None)))
        return True


    '''
    Utility Functions
    '''
    # Note: For each line, returns (constraint that determines line, line)
    def linesFor(self, p, cs):
        lines = list()

        for c in cs:
            pred = c.pred
            ps = c.points
            if pred == "coll":
                other_ps = [p1 for p1 in ps if p1 != p]
                lines.append(([c], Line("connecting", other_ps), list()))
            elif pred == "para":
                (x, (y, z)) = group_pairs(p, ps)
                if x is not None:
                    lines.append(([c], Line("paraAt", [x, y, z]), list()))
            elif pred == "perp":
                (x, (y, z)) = group_pairs(p, ps)
                if x is not None:
                    lines.append(([c], Line("perpAt", [x, y, z]), list()))
            elif pred == "cong":
                w, x, y, z = c.points
                if p == w and p == y:
                    lines.append(([c], Line("mediator", [x, z]), list()))
                elif p == w and p == z:
                    lines.append(([c], Line("mediator", [x, y]), list()))
                elif p == x and p == y:
                    lines.append(([c], Line("mediator", [w, z]), list()))
                elif p == x and p == z:
                    lines.append(([c], Line("mediator", [w, y]), list()))
            elif pred == "ibisector":
                # FIXME: Missing extra sameside constraints (the ndgs)
                p1, x, y, z = c.points
                if p == p1:
                    extra_c1 = Constraint("sameSide", [p1, x, y, z], False)
                    extra_c2 = Constraint("sameSide", [p1, z, y, x], False)
                    lines.append(([c], Line("ibisector", [x, y, z]), [extra_c1, extra_c2]))
            elif pred == "ebisector":
                p1, x, y, z = c.points
                if p == p1:
                    lines.append(([c], Line("ebisector", [x, y, z]), list()))
            elif pred == "eqOAngle":
                u, v, w, x, y, z = c.points
                if u == p and p not in [v, w, x, y, z]:
                    lines.append(([c], Line("eqOAngle", [v, w, x, y, z]), list()))
                elif w == p and p not in [u, v, x, y, z]:
                    lines.append(([c], Line("eqOAngle", [u, v, x, y, z]), list()))
                elif x == p and p not in [u, v, w, y, z]:
                    lines.append(([c], Line("eqOAngle", [u, v, w, y, z]), list()))
                elif z == p and p not in [u, v, w, x, y]:
                    lines.append(([c], Line("eqOAngle", [u, v, w, x, y]), list()))
            elif pred == "onSeg":
                x, y, z = c.points
                extra_c = Constraint("between", [x, y, z], False)
                if p == x:
                    lines.append(([c], Line("connecting", [y, z]), [extra_c]))
                elif p == y:
                    lines.append(([c], Line("connecting", [x, z]), [extra_c]))
                elif p == z:
                    lines.append(([c], Line("connecting", [x, y]), [extra_c]))

        return lines

    def circlesFor(self, p, cs):
        circles = list()

        for c in cs:
            pred = c.pred
            ps = c.points
            if pred == "cycl":
                other_ps = [p1 for p1 in ps if p1 != p]
                circles.append(([c], Circle("c3", other_ps), list()))
            elif pred == "onC":
                p1, o, x = ps
                if p == p1:
                    circles.append(([c], Circle("coa", [o, x]), list()))
            elif pred == "cong":
                if ps.count(p) == 1:
                    (x, (y, z)) = group_pairs(p, ps)
                    if x == y:
                        circles.append(([c], Circle("coa", [x, z]), list()))
                    elif x == z:
                        circles.append(([c], Circle("coa", [x, y]), list()))
                    else:
                        circles.append(([c], Circle("cong", [b, c, d]), list()))
            elif pred == "perp":
                w, x, y, z = ps
                if p == w and p == y:
                    circles.append(([c], Circle("diam", [x, z]), list()))
                elif p == w and p == z:
                    circles.append(([c], Circle("diam", [x, y]), list()))
                elif p == x and p == y:
                    circles.append(([c], Circle("diam", [w, z]), list()))
                elif p == x and p == z:
                    circles.append(([c], Circle("diam", [w, y]), list()))
        return circles

    # Returns (root, constraints to get root)
    # Responsible for updating blacklist and open roots
    def determine_root(self, p, cl1, cl2, cs):
        # FIXME: Should we try for all combos of lines and circles?
        # FIXME: Should key be sorted?

        k = (cl1, cl1) # key
        shared_points = list(set(cl1.pointsOn()).intersection(cl2.pointsOn()))
        oppCs = [c for c in cs if c.pred == "oppSides"]
        sameCs = [c for c in cs if c.pred == "sameSide"]

        if k in self.open_roots: # rsNotPrevious
            root = Root("neq", [self.open_roots[k]]) # FIXME: Check that self.open_roots[k] is a point, not a list
            del self.open_roots[k]
            return (root, list())
        elif shared_points: # rsNeq
            root = Root("neq", [shared_points[0]])
            return (root, list())
        elif oppCs and (oppCs[0].points[0] == p or oppCs[0].points[1] == p):
            a, b, c, d = oppCs[0].points[0], oppCs[0].points[1], oppCs[0].points[2], oppCs[0].points[3]
            if oppCs[0].points[0] == p:
                root = Root("oppSides", [b, Line("connecting", [c, d])])
            else: # oppCs[0].points[1] == p
                root = Root("oppSides", [a, Line("connecting", [c, d])])
            return (root, [oppCs[0]])
        elif sameCs and (sameCs[0].points[0] == p or sameCs[0].points[1] == p):
            a, b, c, d = sameCs[0].points[0], sameCs[0].points[1], sameCs[0].points[2], sameCs[0].points[3]
            if sameCs[0].points[0] == p:
                root = Root("sameSide", [b, Line("connecting", [c, d])])
            else: # sameCs[0].points[1] == p
                root = Root("sameSide", [a, Line("connecting", [c, d])])
            return (root, [sameCs[0]])
        else:
            # rsArbitrary
            if p not in self.root_blacklist:
                self.open_roots[k] = p
                root = Root("arbitrary", list())
                return (root, list())
            else:
                return (None, None)
