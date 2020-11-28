import pdb
import argparse
import math
import numpy as np

from instruction import Assert, AssertNDG, Eval, Sample, Parameterize, Compute
from constraint import Constraint
from parse import parse_sexprs
from primitives import Point, Line, Circle, Num
from util import Root, is_number, FuncInfo

RESERVED_NAMES = ["pi"]


class InstructionReader:
    def __init__(self, problem_lines):
        self.points = list()
        self.circles = list()
        self.lines = list()

        self.instructions = list()
        self.problem_lines = problem_lines

        self.unnamed_points = list()
        self.unnamed_lines = list()
        self.unnamed_circles = list()
        self.segments = list()
        self.seg_colors = list()

        cmds = parse_sexprs(self.problem_lines)
        for cmd in cmds:
            try:
                self.process_command(cmd)
            except:
                raise RuntimeError(f"Invalid command: {cmd}")

    def register_pt(self, p):
        if p in self.points:
            raise RuntimeError(f"[register_pt] Same point declared twice: {p}")
        if not (isinstance(p, Point) and isinstance(p.val, str)):
            raise RuntimeError(f"[register_pt] Invalid point: {p}")
        if p.val.lower() in RESERVED_NAMES:
            raise RuntimeError(f"[register_pt] Reserved name: {p}")
        self.points.append(p)

    def register_circ(self, c):
        if c in self.circles:
            raise RuntimeError(f"[register_circ] Same circle declared twice: {c}")
        if not (isinstance(c, Circle) and isinstance(c.val, str)):
            raise RuntimeError(f"[register_circ] Invalid circle name: {c.val}")
        if c.val.lower() in RESERVED_NAMES:
            raise RuntimeError(f"[register_circ] Reserved name: {c}")
        self.circles.append(c)

    def register_line(self, l):
        if l in self.lines:
            raise RuntimeError(f"[register_line] Same line declared twice: {l}")
        if not (isinstance(l, Line) and isinstance(l.val, str)):
            raise RuntimeError(f"[register_line] Invalid line name: {l.val}")
        if l.val.lower() in RESERVED_NAMES:
            raise RuntimeError(f"[register_line] Reserved name: {l}")
        self.lines.append(l)

    def process_command(self, cmd):
        if not isinstance(cmd[0], str):
            raise RuntimeError(f"[process_cmd] command must be a string")
        head = cmd[0].lower()
        if head == "assert":
            self.add(cmd)
        elif head == "let":
            self.compute(cmd)
        elif head == "eval":
            self.eval_cons(cmd)
        elif head == "param":
            if isinstance(cmd[1], str):
                self.param(cmd)
            elif isinstance(cmd[1], tuple):
                self.process_param_special(cmd)
            else:
                raise RuntimeError("Invalid param input type")
        else:
            raise NotImplementedError(f"[InstructionReader.process_command] Command not supported: {head}")


    # def sample(self, cmd):
    def process_param_special(self, cmd):

        assert(len(cmd) == 3)

        ps = [Point(p) for p in cmd[1]]
        for p in ps:
            self.register_pt(p)

        param_method = cmd[2]

        if isinstance(param_method, str):
            p_method = param_method.lower()
            assert(p_method in ["triangle", "acute-tri", "equi-tri", "polygon"])
            instr = Sample(ps, p_method) # No extra args here
            self.instructions.append(instr)
        elif isinstance(param_method, tuple):
            assert(len(param_method) == 2)
            head, arg = param_method
            head = head.lower()
            assert(head in ["right-tri", "iso-tri", "acute-iso-tri"])
            assert(isinstance(arg, str) and Point(arg) in ps)
            special_p = Point(arg) # Not coming in as Point
            instr = Sample(ps, head, (special_p,))
            self.instructions.append(instr)
        else:
            raise RuntimeError("Invalid joint param method")

        n_gon_color = np.random.rand(3)
        for i in range(len(ps)):
            self.segments.append((ps[i], ps[(i+1) % (len(ps))]))
            self.seg_colors.append(n_gon_color)


    def compute(self, cmd):
        assert(len(cmd) == 4)

        obj_name = cmd[1]
        assert(isinstance(obj_name, str))

        obj_type = cmd[2].lower()
        assert(obj_type in ["point", "line", "circle"])

        if obj_type == "point":
            p = Point(obj_name)
            self.register_pt(p)

            computation = self.process_point(cmd[3], unnamed=False)
            assert(not isinstance(computation.val, str))

            c_instr = Compute(p, computation)
            self.instructions.append(c_instr)
        elif obj_type == "line":
            l = Line(obj_name)
            self.register_line(l)

            computation = self.process_line(cmd[3], unnamed=False)
            assert(not isinstance(computation.val, str))

            c_instr = Compute(l, computation)
            self.instructions.append(c_instr)

        elif obj_type == "circle":
            c = Circle(obj_name)
            self.register_circ(c)

            computation = self.process_circle(cmd[3], unnamed=False)
            assert(not isinstance(computation.val, str))

            c_instr = Compute(c, computation)
            self.instructions.append(c_instr)

        else:
            raise RuntimeError("Invalid let type")



    def add(self, cmd):
        assert(len(cmd) == 2)
        negate, pred, args = self.process_constraint(cmd[1])

        instr_cons = Constraint(pred, args, False)
        if negate:
            self.instructions.append(AssertNDG(instr_cons))
        else:
            self.instructions.append(Assert(instr_cons))


    def eval_cons(self, cmd):
        assert(len(cmd) == 2)
        negate, pred, args = self.process_constraint(cmd[1])
        instr_cons = Constraint(pred, args, negate)
        self.instructions.append(Eval(instr_cons))

    def param(self, cmd):
        assert(len(cmd) == 3 or len(cmd) == 4)

        obj_type = cmd[2].lower()
        assert(obj_type in ["point", "line", "circle"])

        if obj_type == "line":
            l = Line(cmd[1])
            self.register_line(l)

            param_method = "line"
            if len(cmd) == 4:
                param_method = cmd[3]
            pred, args = self.process_param_line(param_method)
            p_instr = Parameterize(l, (pred, args))
            self.instructions.append(p_instr)
        elif obj_type == "circle":
            c = Circle(cmd[1])
            self.register_circ(c)

            param_method = "circle"
            if len(cmd) == 4:
                param_method = cmd[3]
            pred, args = self.process_param_circ(param_method)
            p_instr = Parameterize(c, (pred, args))
            self.instructions.append(p_instr)
        else:
            p = Point(cmd[1])
            self.register_pt(p)

            param_method = "coords"
            if len(cmd) == 4:
                param_method = cmd[3]
            pred, args = self.process_param_point(param_method)
            p_instr = Parameterize(p, (pred, args))
            self.instructions.append(p_instr)

    def process_param_circ(self, param):
        if isinstance(param, str) and param.lower() == "circle":
            return "circle", None

        pred = param[0].lower()
        args = param[1:]
        args = [self.process_term(t) for t in args]

        if pred == "origin":
            assert(len(args) == 1)
            assert(isinstance(args[0], Point))
        elif pred == "radius":
            assert(len(args) == 1)
            assert(isinstance(args[0], Num))
        elif pred == "through":
            assert(len(args) == 1)
            assert(isinstance(args[0], Point))
            pred = "through-c"
        elif pred == "tangent-cc":
            assert(len(args) == 1)
            assert(isinstance(args[0], Circle))
        elif pred == "tangent-cl":
            assert(len(args) == 1)
            assert(isinstance(args[0], Line))
        else:
            raise NotImplementedError(f"[process_param_circ] unrecognized param {param}")
        return pred, args

    def process_param_line(self, param):
        if isinstance(param, str) and param.lower() == "line":
            return "line", None

        pred = param[0].lower()
        args = param[1:]
        args = [self.process_term(t) for t in args]

        if pred == "through":
            assert(len(args) == 1)
            assert(isinstance(args[0], Point))
            pred = "through-l"
        elif pred == "tangent-lc":
            assert(len(args) == 1)
            assert(isinstance(args[0], Circle))
        else:
            raise NotImplementedError(f"[process_param_line] unrecognized param {param}")
        return pred, args


    def process_param_point(self, param):
        if isinstance(param, str) and param.lower() == "coords":
            return "coords", None

        pred = param[0].lower()
        args = param[1:]
        args = [self.process_term(t) for t in args]

        ps = [t for t in args if isinstance(t, Point)]
        ls = [t for t in args if isinstance(t, Line)]
        cs = [t for t in args if isinstance(t, Circle)]

        if pred == "on-seg":
            assert(len(args) == 2)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "on-line":
            assert(len(args) == 1)
            assert(all([isinstance(t, Line) for t in args]))
        elif pred in ["on-ray", "on-ray-opp"]:
            assert(len(args) == 2)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "on-circ":
            assert(len(args) == 1)
            assert(all([isinstance(t, Circle) for t in args]))
        elif pred == "in-poly":
            assert(len(args) >= 3)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred in ["on-minor-arc", "on-major-arc"]:
            assert(len(args) == 3)
            assert(isinstance(args[0], Circle))
            assert(isinstance(args[1], Point))
            assert(isinstance(args[2], Point))
        else:
            raise NotImplementedError(f"[process_param_point] unrecognized param {param}")
        return pred, args


    def process_constraint(self, constraint):
        assert(isinstance(constraint, tuple))

        negate = (isinstance(constraint[0], str) and constraint[0].lower() == "not")
        if negate:
            constraint = constraint[1]

        pred = constraint[0].lower()
        args = constraint[1:]

        args = [self.process_term(t) for t in args]

        ps = [t for t in args if isinstance(t, Point)]
        ls = [t for t in args if isinstance(t, Line)]
        cs = [t for t in args if isinstance(t, Circle)]
        ns = [t for t in args if isinstance(t, Num)]

        # Validate
        if pred in ["circumcenter", "orthocenter", "incenter", "centroid"]:
            assert(len(args) == 4)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred in ["con-tri", "sim-tri"]:
            assert(len(args) == 6)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "coll":
            assert(len(args) == 3)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "concur":
            assert(len(args) == 3)
            assert(all([isinstance(t, Line) for t in args]))
        elif pred == "cong":
            assert(len(args) == 4)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "cycl":
            assert(len(args) >= 4)
            assert(all([isinstance(t, Point) for t in args]))
            self.unnamed_circles.append(Circle(FuncInfo("c3", args[:3])))
        elif pred == "eq" or pred == "=":
            assert(len(args) == 2)
            if all([isinstance(t, Num) for t in args]):
                pred = "eq-n"
            elif all([isinstance(t, Point) for t in args]):
                pred = "eq-p"
            elif all([isinstance(t, Line) for t in args]):
                pred = "eq-l"
            else:
                raise RuntimeError("Invalid usage of eq")
        elif pred == "foot":
            assert(len(args) == 3)
            assert(isinstance(args[0], Point) and isinstance(args[1], Point))
            assert(isinstance(args[2], Line))
        elif pred == "gt" or pred == ">":
            pred = "gt"
            assert(len(args) == 2)
            assert(all([isinstance(t, Num) for t in args]))
        elif pred == "gte" or pred == ">=":
            pred = "gte"
            assert(len(args) == 2)
            assert(all([isinstance(t, Num) for t in args]))
        elif pred == "lt" or pred == "<":
            pred = "lt"
            assert(len(args) == 2)
            assert(all([isinstance(t, Num) for t in args]))
        elif pred == "lte" or pred == "<=":
            pred = "lte"
            assert(len(args) == 2)
            assert(all([isinstance(t, Num) for t in args]))
        # elif pred == "eq-angle":
            # assert(len(args) == 8)
            # assert(all([isinstance(t, Point) for t in args]))
        elif pred == "eq-ratio":
            assert(len(args) == 8)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "i-bisector":
            assert(len(args) == 4)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "inter-ll":
            assert(len(args) == 5)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "in-poly":
            assert(len(args) >= 4)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "midp":
            assert(len(args) == 3)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "on-line":
            assert(len(args) == 2)
            assert(isinstance(args[0], Point) and isinstance(args[1], Line))
        elif pred in ["on-seg", "on-ray"]: # no more between
            assert(len(args) == 3)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "on-circ":
            assert(len(args) == 2)
            assert(isinstance(args[0], Point) and isinstance(args[1], Circle))
        elif pred == "opp-sides":
            assert(len(args) == 3)
            assert(isinstance(args[0], Point) and isinstance(args[1], Point))
            assert(isinstance(args[2], Line))
        elif pred == "para" or pred == "perp":
            assert(len(args) == 2)
            assert(all([isinstance(t, Line) for t in args]))
        elif pred in ["right", "right-tri"]:
            assert(len(args) == 3)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "reflect-pl":
            assert(len(args) == 4)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "same-side":
            assert(len(args) == 3)
            assert(isinstance(args[0], Point) and isinstance(args[1], Point))
            assert(isinstance(args[2], Line))
        elif pred == "tangent-cc":
            assert(len(args) == 2)
            assert(all([isinstance(t, Circle) for t in args]))
        elif pred == "tangent-lc":
            assert(len(args) == 2)
            assert(isinstance(args[0], Line) and isinstance(args[1], Circle))
        elif pred == "tangent-at-cc":
            assert(len(args) == 3)
            assert(isinstance(args[0], Point))
            assert(isinstance(args[1], Circle) and isinstance(args[2], Circle))
        elif pred == "tangent-at-lc":
            assert(len(args) == 3)
            assert(isinstance(args[0], Point))
            assert(isinstance(args[1], Line) and isinstance(args[2], Circle))
        else:
            raise NotImplementedError(f"[process_constraint] Unsupported pred {pred}")

        return negate, pred, args

    def process_term(self, term):
        try:
            return self.process_point(term)
        except:
            try:
                return self.process_line(term)
            except:
                try:
                    return self.process_circle(term)
                except:
                    try:
                        return self.process_number(term)
                    except:
                        raise RuntimeError(f"Term {term} not a point/line/circle")

    def process_point(self, p_info, unnamed=True):
        if isinstance(p_info, str) and not is_number(p_info):
            assert(Point(p_info) in self.points)
            return Point(p_info)
        if not isinstance(p_info, tuple):
            raise NotImplementedError(f"[process_point] p_info must be tuple or string")

        p_pred = p_info[0].lower()
        p_args = p_info[1:]

        p_val = None

        if p_pred == "inter-ll":
            assert(len(p_args) == 2)
            l1 = self.process_line(p_args[0])
            l2 = self.process_line(p_args[1])
            p_val = FuncInfo(p_pred, (l1, l2))
        elif p_pred in ["isogonal-conj", "isotomic-conj"]:
            assert(len(p_args) == 4)
            ps = [self.process_point(p) for p in p_args]
            p_val = FuncInfo(p_pred, tuple(ps))
        elif p_pred == "harmonic-conj":
            assert(len(p_args) == 3)
            ps = [self.process_point(p) for p in p_args]
            p_val = FuncInfo(p_pred, tuple(ps))
        elif p_pred in ["incenter", "excenter", "mixtilinear-incenter"]:
            assert(len(p_args) == 3)
            ps = [self.process_point(p) for p in p_args]
            p_val = FuncInfo(p_pred, tuple(ps))
        elif p_pred == "inter-lc":
            assert(len(p_args) == 3)
            l = self.process_line(p_args[0])
            c = self.process_circle(p_args[1])
            rs = self.process_rs(p_args[2])
            p_val = FuncInfo(p_pred, (l, c, rs))
        elif p_pred == "inter-cc":
            assert(len(p_args) == 3)
            c1 = self.process_circle(p_args[0])
            c2 = self.process_circle(p_args[1])
            rs = self.process_rs(p_args[2])
            p_val = FuncInfo(p_pred, (c1, c2, rs))
        elif p_pred in ["midp", "midp-from"]:
            assert(len(p_args) == 2)
            ps = [self.process_point(p) for p in p_args]
            p_val = FuncInfo(p_pred, tuple(ps))
        elif p_pred == "foot":
            assert(len(p_args) == 2)
            p = self.process_point(p_args[0])
            l = self.process_line(p_args[1])
            p_val = FuncInfo(p_pred, (p, l))
        elif p_pred == "reflect-pl":
            assert(len(p_args) == 2)
            p = self.process_point(p_args[0])
            l = self.process_line(p_args[1])
            p_val = FuncInfo(p_pred, (p, l))
        elif p_pred in ["orthocenter", "circumcenter", "centroid", "incenter"]:
            assert(len(p_args) == 3)
            ps = [self.process_point(p) for p in p_args]
            p_val = FuncInfo(p_pred, tuple(ps))
        elif p_pred == "origin":
            assert(len(p_args) == 1)
            circ = self.process_circle(p_args[0])
            p_val = FuncInfo(p_pred, (circ,))
        elif p_pred in ["amidp-opp", "amidp-same"]:
            assert(len(p_args) == 3)
            ps = [self.process_point(p) for p in p_args]
            p_val = FuncInfo(p_pred, tuple(ps))

        if p_val is not None:
            P = Point(p_val)
            if unnamed:
                self.unnamed_points.append(P)
            return P
        else:
            raise NotImplementedError(f"[process_point] Unrecognized p_pred {p_pred}")


    def process_line(self, l_info, unnamed=True):
        if isinstance(l_info, str) and not is_number(l_info):
            assert(Line(l_info) in self.lines)
            return Line(l_info)
        if not isinstance(l_info, tuple):
            raise NotImplementedError(f"[process_line] l_info must be tuple or string")

        l_pred = l_info[0].lower()
        l_args = l_info[1:]

        l_val = None

        if l_pred == "line":
            assert(len(l_args) == 2)
            ps = [self.process_point(p) for p in l_args]
            l_val = FuncInfo("connecting", ps)
        elif l_pred in ["perp-at", "para-at"]:
            assert(len(l_args) == 2)
            p = self.process_point(l_args[0])
            l = self.process_line(l_args[1])
            l_val = FuncInfo(l_pred, [p, l])
        elif l_pred == "perp-bis":
            assert(len(l_args) == 2)
            ps = [self.process_point(p) for p in l_args]
            l_val = FuncInfo(l_pred, ps)
        elif l_pred in ["isogonal", "isotomic"]:
            assert(len(l_args) == 4)
            ps = [self.process_point(p) for p in l_args]
            l_val = FuncInfo(l_pred, ps)
        elif l_pred in ["i-bisector", "e-bisector"]:
            assert(len(l_args) == 3)
            ps = [self.process_point(p) for p in l_args]
            l_val = FuncInfo(l_pred, ps)
        elif l_pred == "reflect-ll":
            assert(len(l_args) == 2)
            ls = [self.process_line(l) for l in l_args]
            l_val = FuncInfo(l_pred, ls)

        if l_val is not None:
            L = Line(l_val)
            if unnamed:
                self.unnamed_lines.append(L)
            return L
        else:
            raise NotImplementedError(f"[process_line] Unsupported line pred: {l_pred}")

    def process_circle(self, c_info, unnamed=True):
        if isinstance(c_info, str) and not is_number(c_info):
            assert(Circle(c_info) in self.circles)
            return Circle(c_info)
        if not isinstance(c_info, tuple):
            raise NotImplementedError(f"[process_circle] c_info must be tuple or string")

        c_pred = c_info[0].lower()
        ps = [self.process_point(p) for p in c_info[1:]]
        c_val = None

        if c_pred == "circ":
            assert(len(ps) == 3)
            c_val = FuncInfo("c3", ps)
        elif c_pred == "coa":
            assert(len(ps) == 2)
            c_val = FuncInfo(c_pred, ps)
        elif c_pred == "diam":
            assert(len(ps) == 2)
            c_val = FuncInfo("diam", ps)
        elif c_pred == "circumcircle":
            assert(len(ps) == 3)
            c_val = FuncInfo("circumcircle", ps)
        elif c_pred == "incircle":
            assert(len(ps) == 3)
            c_val = FuncInfo("incircle", ps)
        elif c_pred == "excircle":
            assert(len(ps) == 3)
            c_val = FuncInfo("excircle", ps)
        elif c_pred == "mixtilinear-incircle":
            assert(len(ps) == 3)
            c_val = FuncInfo(c_pred, ps)

        if c_val is not None:
            C = Circle(c_val)
            if unnamed:
                self.unnamed_circles.append(C)
            return C
        else:
            raise NotImplementedError(f"[process_circle] Unsupported circle pred: {c_pred}")

    def process_number(self, n_info):
        if isinstance(n_info, str) and n_info.lower() == "pi":
            return Num(math.pi)
        if isinstance(n_info, str) and is_number(n_info):
            return Num(float(n_info))
        if not isinstance(n_info, tuple):
            raise NotImplementedError(f"[process_number] n_info must be tuple or string")

        n_pred = n_info[0].lower()
        n_args = n_info[1:]

        if n_pred == "dist":
            assert(len(n_args) == 2)
            p1 = self.process_point(n_args[0])
            p2 = self.process_point(n_args[1])
            n_val = FuncInfo("dist", [p1, p2])
            return Num(n_val)
        elif n_pred in ["uangle", "area"]:
            assert(len(n_args) == 3)
            p1, p2, p3 = [self.process_point(p) for p in n_args]
            n_val = FuncInfo(n_pred, [p1, p2, p3])
            return Num(n_val)
        elif n_pred == "radius":
            assert(len(n_args) == 1)
            circ = self.process_circle(n_args[0])
            n_val = FuncInfo("radius", [circ])
            return Num(n_val)
        elif n_pred == "diam":
            assert(len(n_args) == 1)
            circ = self.process_circle(n_args[0])
            n_val = FuncInfo("diam", [circ])
            return Num(n_val)
        elif n_pred in ["div", "add", "sub", "mul", "pow"]:
            assert(len(n_args) == 2)
            n1, n2 = [self.process_number(n) for n in n_args]
            n_val = FuncInfo(n_pred, [n1, n2])
            return Num(n_val)
        elif n_pred in ["neg", "sqrt"]:
            assert(len(n_args) == 1)
            n = self.process_number(n_args[0])
            n_val = FuncInfo(n_pred, [n])
            return Num(n_val)
        else:
            raise NotImplementedError(f"[process_number] Unsupporrted number pred: {n_pred}")


    def process_rs(self, rs_info):

        if isinstance(rs_info, str) and rs_info.lower() == "rs-arbitrary":
            return Root("arbitrary", list())

        rs_pred = rs_info[0].lower()
        rs_args = rs_info[1:]

        if rs_pred == "rs-neq":
            assert(len(rs_args) == 1)
            p_neq = self.process_point(rs_args[0])
            return Root("neq", [p_neq])
        elif rs_pred == "rs-closer-to-p":
            assert(len(rs_args) == 1)
            p_neq = self.process_point(rs_args[0])
            return Root("closer-to-p", [p_neq])
        elif rs_pred == "rs-closer-to-l":
            assert(len(rs_args) == 1)
            p_neq = self.process_line(rs_args[0])
            return Root("closer-to-l", [p_neq])
        elif rs_pred == "rs-opp-sides":
            assert(len(rs_args) == 2)
            opp_p = self.process_point(rs_args[0])
            dividing_line = self.process_line(rs_args[1])
            return Root("opp-sides", [opp_p, dividing_line])
        else:
            raise NotImplementedError(f"[process_rs] Unsupported rs pred: {rs_pred}")

    # Utilities
    def assert_all_points(self, ps):
        assert(all([isinstance(t, Point) for t in ps]))

    def assert_all_lines(self, ls):
        assert(all([isinstance(t, Line) for t in ls]))

    def assert_all_circles(self, cs):
        assert(all([isinstance(t, Circle) for t in cs]))


if __name__ == "__main__":
    # Get problem to compile
    parser = argparse.ArgumentParser(description='Arguments for compiling a file of instructions to an instruction set')
    parser.add_argument('--problem', '-p', action='store', type=str, help='Name of the file defining the set of constraints')

    args = parser.parse_args()
    lines = open(args.problem, 'r').readlines()

    reader = InstructionReader(lines)
    instructions = reader.instructions

    for instr in instructions:
        print(instr)
