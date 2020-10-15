import pdb
import argparse
import math

from instruction import Assert, AssertNDG, Confirm, Sample, Parameterize, Compute
from constraint import Constraint
from parse import parse_sexprs
from primitives import Point, Line, Circle, Num
from util import Root, is_number, FuncInfo, CASE_FIX

RESERVED_NAMES = ["pi"]


class InstructionReader:
    def __init__(self, problem_lines):
        self.points = list()
        self.circles = list()
        self.lines = list()

        self.instructions = list()
        self.problem_lines = problem_lines

        self.problem_type = None

        self.unnamed_points = list()
        self.unnamed_lines = list()
        self.unnamed_circles = list()
        self.segments = list()

        cmds = parse_sexprs(self.problem_lines)
        for cmd in cmds:
            self.process_command(cmd)

    def update_problem_type(self, p_type):
        if p_type not in ["compile", "instructions"]:
            raise RuntimeError(f"Invalid problem type: {p_type}")
        if self.problem_type == "compile" and p_type == "instructions":
            raise RuntimeError(f"Invalid problem statement")
        elif self.problem_type == "instructions" and p_type == "compile":
            raise RuntimeError(f"Invalid problem statement")
        self.problem_type = p_type

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
        if head == "sample":
            raise NotImplementedError("Sample is deprecated")
            # self.sample(cmd)
            # self.update_problem_type("instructions")
        elif head == "assert":
            self.add(cmd)
        elif head == "compute":
            self.compute(cmd)
            self.update_problem_type("instructions")
        elif head == "confirm":
            self.confirm(cmd)
        elif head == "param":
            if isinstance(cmd[1], str):
                self.param(cmd)
            elif isinstance(cmd[1], tuple):
                self.process_param_special(cmd)
            else:
                raise RuntimeError("Invalid param input type")
            self.update_problem_type("instructions")
        elif head == "declare-points":
            assert(len(cmd) > 1)
            ps = cmd[1:]
            for p in ps:
                self.register_pt(Point(p))
            self.update_problem_type("compile")
        elif head == "declare-point":
            assert(len(cmd) == 2)
            p = cmd[1]
            self.register_pt(Point(p))
            self.update_problem_type("compile")
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
            assert(param_method.lower() in ["triangle", "acutetri", "equitri", "polygon"])
            instr = Sample(ps, CASE_FIX[param_method.lower()]) # No extra args here
            self.instructions.append(instr)
        elif isinstance(param_method, tuple):
            assert(len(param_method) == 2)
            head, arg = param_method
            assert(head.lower() in ["righttri", "isotri", "acuteisotri"])
            assert(isinstance(arg, str) and Point(arg) in ps)
            special_p = Point(arg) # Not coming in as Point
            instr = Sample(ps, CASE_FIX[head.lower()], (special_p,))
            self.instructions.append(instr)
        else:
            raise RuntimeError("Invalid joint param method")

        for i in range(len(ps)):
            self.segments.append((ps[i], ps[(i+1) % (len(ps))]))


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
            raise RuntimeError("Invalid compute type")



    def add(self, cmd):
        assert(len(cmd) == 2)
        negate, pred, args = self.process_constraint(cmd[1])

        instr_cons = Constraint(pred, args, False)
        if negate:
            self.instructions.append(AssertNDG(instr_cons))
        else:
            self.instructions.append(Assert(instr_cons))


    def confirm(self, cmd):
        assert(len(cmd) == 2)
        negate, pred, args = self.process_constraint(cmd[1])
        instr_cons = Constraint(pred, args, negate)
        self.instructions.append(Confirm(instr_cons))

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
            return CASE_FIX[param.lower()], None

        pred = param[0].lower()
        args = param[1:]
        args = [self.process_term(t) for t in args]

        if pred == "origin":
            assert(len(args) == 1)
            assert(isinstance(args[0], Point))
        elif pred == "radius":
            assert(len(args) == 1)
            assert(isinstance(args[0], Num))
        elif pred == "throughc":
            assert(len(args) == 1)
            assert(isinstance(args[0], Point))
        elif pred == "tangentcc":
            assert(len(args) == 1)
            assert(isinstance(args[0], Circle))
        elif pred == "tangentcl":
            assert(len(args) == 1)
            assert(isinstance(args[0], Line))
        else:
            raise NotImplementedError(f"[process_param_circ] unrecognized param {param}")
        return CASE_FIX[pred], args

    def process_param_line(self, param):
        if isinstance(param, str) and param.lower() == "line":
            return CASE_FIX[param.lower()], None

        pred = param[0].lower()
        args = param[1:]
        args = [self.process_term(t) for t in args]

        if pred == "throughl":
            assert(len(args) == 1)
            assert(isinstance(args[0], Point))
        elif pred == "tangentlc":
            assert(len(args) == 1)
            assert(isinstance(args[0], Circle))
        else:
            raise NotImplementedError(f"[process_param_line] unrecognized param {param}")
        return CASE_FIX[pred], args


    def process_param_point(self, param):
        if isinstance(param, str) and param.lower() == "coords":
            return CASE_FIX[param.lower()], None

        pred = param[0].lower()
        args = param[1:]
        args = [self.process_term(t) for t in args]

        ps = [t for t in args if isinstance(t, Point)]
        ls = [t for t in args if isinstance(t, Line)]
        cs = [t for t in args if isinstance(t, Circle)]

        if pred == "onseg":
            assert(len(args) == 2)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "online":
            assert(len(args) == 1)
            assert(all([isinstance(t, Line) for t in args]))
        elif pred in ["onray", "onrayopp"]:
            assert(len(args) == 2)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "oncirc":
            assert(len(args) == 1)
            assert(all([isinstance(t, Circle) for t in args]))
        elif pred == "inpoly":
            assert(len(args) >= 3)
            assert(all([isinstance(t, Point) for t in args]))
        else:
            raise NotImplementedError(f"[process_param_point] unrecognized param {param}")
        return CASE_FIX[pred], args


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
        elif pred == "eqn" or pred == "=":
            pred = "eqN"
            assert(len(args) == 2)
            assert(all([isinstance(t, Num) for t in args]))
        elif pred == "eqp" or pred == "=":
            pred = "eqP"
            assert(len(args) == 2)
            assert(all([isinstance(t, Point) for t in args]))
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
        # elif pred == "eqangle":
            # assert(len(args) == 8)
            # assert(all([isinstance(t, Point) for t in args]))
        elif pred == "eqratio":
            assert(len(args) == 8)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "ibisector":
            assert(len(args) == 4)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "interll":
            assert(len(args) == 5)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "inpoly":
            assert(len(args) >= 4)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "midp":
            assert(len(args) == 3)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "online":
            assert(len(args) == 2)
            assert(isinstance(args[0], Point) and isinstance(args[1], Line))
        elif pred in ["onseg", "onray", "between"]:
            assert(len(args) == 3)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "oncirc":
            assert(len(args) == 2)
            assert(isinstance(args[0], Point) and isinstance(args[1], Circle))
        elif pred == "oppsides":
            assert(len(args) == 3)
            assert(isinstance(args[0], Point) and isinstance(args[1], Point))
            assert(isinstance(args[2], Line))
        elif pred == "para" or pred == "perp":
            if len(args) == 2:
                assert(all([isinstance(t, Line) for t in args]))
            elif len(args) == 4:
                assert(all([isinstance(t, Point) for t in args]))
            else:
                raise RuntimeError(f"Invalid para constraint {constraint}")
        elif pred == "right":
            assert(len(args) == 3)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "reflectpl":
            assert(len(args) == 4)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "sameside":
            assert(len(args) == 3)
            assert(isinstance(args[0], Point) and isinstance(args[1], Point))
            assert(isinstance(args[2], Line))
        elif pred == "tangentcc":
            assert(len(args) == 2)
            assert(all([isinstance(t, Circle) for t in args]))
        elif pred == "tangentlc":
            assert(len(args) == 2)
            assert(isinstance(args[0], Line) and isinstance(args[1], Circle))
        elif pred == "tangentatcc":
            assert(len(args) == 3)
            assert(isinstance(args[0], Point))
            assert(isinstance(args[1], Circle) and isinstance(args[2], Circle))
        elif pred == "tangentatlc":
            assert(len(args) == 3)
            assert(isinstance(args[0], Point))
            assert(isinstance(args[1], Line) and isinstance(args[2], Circle))
        else:
            raise NotImplementedError(f"[process_constraint] Unsupported pred {pred}")

        return negate, CASE_FIX[pred], args

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

        p_pred_lower = p_info[0].lower()
        p_pred = CASE_FIX[p_pred_lower]
        p_args = p_info[1:]

        p_val = None

        if p_pred_lower in ["amidpopp", "amidpsame"]:
            assert(len(p_args) == 4)
            ps = [self.process_point(p) for p in p_args]
            p_val = FuncInfo(p_pred, tuple(ps))
        elif p_pred_lower == "interll":
            assert(len(p_args) == 2)
            l1 = self.process_line(p_args[0])
            l2 = self.process_line(p_args[1])
            p_val = FuncInfo(p_pred, (l1, l2))
            """
            elif len(p_args) == 4:
                p1, p2, p3, p4 = [self.process_point(p) for p in p_args]
                l1 = Line(FuncInfo("connecting", [p1, p2]))
                l2 = Line(FuncInfo("connecting", [p3, p4]))
                p_val = FuncInfo("interLL", (l1, l2))
            """
        elif p_pred_lower in ["isogonalconj", "isotomicconj"]:
            assert(len(p_args) == 4)
            ps = [self.process_point(p) for p in p_args]
            p_val = FuncInfo(p_pred, tuple(ps))
        elif p_pred_lower == "harmonicconj":
            assert(len(p_args) == 3)
            ps = [self.process_point(p) for p in p_args]
            p_val = FuncInfo(p_pred, tuple(ps))
        elif p_pred_lower in ["incenter", "excenter", "mixtilinearincenter"]:
            assert(len(p_args) == 3)
            ps = [self.process_point(p) for p in p_args]
            p_val = FuncInfo(p_pred, tuple(ps))
        elif p_pred_lower == "interlc":
            assert(len(p_args) == 3)
            l = self.process_line(p_args[0])
            c = self.process_circle(p_args[1])
            rs = self.process_rs(p_args[2])
            p_val = FuncInfo("interLC", (l, c, rs))
        elif p_pred_lower == "intercc":
            assert(len(p_args) == 3)
            c1 = self.process_circle(p_args[0])
            c2 = self.process_circle(p_args[1])
            rs = self.process_rs(p_args[2])
            p_val = FuncInfo("interCC", (c1, c2, rs))
        elif p_pred_lower in ["midp", "midpfrom"]:
            assert(len(p_args) == 2)
            ps = [self.process_point(p) for p in p_args]
            p_val = FuncInfo(p_pred, tuple(ps))
        elif p_pred_lower == "reflectpl":
            assert(len(p_args) == 2)
            p = self.process_point(p_args[0])
            l = self.process_line(p_args[1])
            p_val = FuncInfo(p_pred, (p, l))
        elif p_pred_lower in ["orthocenter", "circumcenter", "centroid", "incenter"]:
            assert(len(p_args) == 3)
            ps = [self.process_point(p) for p in p_args]
            p_val = FuncInfo(p_pred, tuple(ps))
        elif p_pred_lower == "origin":
            assert(len(p_args) == 1)
            circ = self.process_circle(p_args[0])
            p_val = FuncInfo("origin", (circ,))
        elif p_pred_lower in ["amidpopp", "amidpsame"]:
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

        l_pred_lower = l_info[0].lower()
        l_pred = CASE_FIX[l_pred_lower]
        l_args = l_info[1:]

        l_val = None

        if l_pred_lower == "line":
            assert(len(l_args) == 2)
            ps = [self.process_point(p) for p in l_args]
            l_val = FuncInfo("connecting", ps)
        elif l_pred_lower in ["perpat", "paraat", "foot"]:
            assert(len(l_args) == 2)
            p = self.process_point(l_args[0])
            l = self.process_line(l_args[1])
            l_val = FuncInfo(CASE_FIX[l_pred_lower], [p, l])
        elif l_pred_lower == "perpbis":
            assert(len(l_args) == 2)
            ps = [self.process_point(p) for p in l_args]
            l_val = FuncInfo("perpBis", ps)
        elif l_pred_lower in ["isogonal", "isotomic"]:
            assert(len(l_args) == 4)
            ps = [self.process_point(p) for p in l_args]
            l_val = FuncInfo(CASE_FIX[l_pred_lower], ps)
        elif l_pred_lower == "ibisector":
            assert(len(l_args) == 3)
            ps = [self.process_point(p) for p in l_args]
            l_val = FuncInfo("ibisector", ps)
        elif l_pred_lower == "ebisector":
            assert(len(l_args) == 3)
            ps = [self.process_point(p) for p in l_args]
            l_val = FuncInfo("ebisector", ps)
        elif l_pred_lower == "reflectll":
            assert(len(l_args) == 2)
            ls = [self.process_line(l) for l in l_args]
            l_val = FuncInfo("reflectLL", ls)

        if l_val is not None:
            self.update_problem_type("instructions")
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

        c_pred_lower = c_info[0].lower()
        c_pred = CASE_FIX[c_pred_lower]
        ps = [self.process_point(p) for p in c_info[1:]]
        c_val = None

        if c_pred_lower == "circ":
            assert(len(ps) == 3)
            c_val = FuncInfo("c3", ps)
        elif c_pred_lower == "coa":
            assert(len(ps) == 2)
            c_val = FuncInfo("coa", ps)
        elif c_pred_lower == "diam":
            assert(len(ps) == 2)
            c_val = FuncInfo("diam", ps)
        elif c_pred_lower == "circumcircle":
            assert(len(ps) == 3)
            c_val = FuncInfo("circumcircle", ps)
        elif c_pred_lower == "incircle":
            assert(len(ps) == 3)
            c_val = FuncInfo("incircle", ps)
        elif c_pred_lower == "excircle":
            assert(len(ps) == 3)
            c_val = FuncInfo("excircle", ps)
        elif c_pred_lower == "mixtilinearincircle":
            assert(len(ps) == 3)
            c_val = FuncInfo("mixtilinearIncircle", ps)

        if c_val is not None:
            self.update_problem_type("instructions")
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

        n_pred_lower = n_info[0].lower()
        n_pred = CASE_FIX[n_pred_lower]
        n_args = n_info[1:]

        if n_pred_lower == "dist":
            assert(len(n_args) == 2)
            p1 = self.process_point(n_args[0])
            p2 = self.process_point(n_args[1])
            n_val = FuncInfo("dist", [p1, p2])
            return Num(n_val)
        elif n_pred_lower in ["uangle", "area"]:
            assert(len(n_args) == 3)
            p1, p2, p3 = [self.process_point(p) for p in n_args]
            n_val = FuncInfo(n_pred, [p1, p2, p3])
            return Num(n_val)
        elif n_pred_lower == "radius":
            assert(len(n_args) == 1)
            circ = self.process_circle(n_args[0])
            n_val = FuncInfo("radius", [circ])
            return Num(n_val)
        elif n_pred_lower == "diam":
            assert(len(n_args) == 1)
            circ = self.process_circle(n_args[0])
            n_val = FuncInfo("diam", [circ])
            return Num(n_val)
        elif n_pred_lower in ["div", "add", "sub", "mul", "pow"]:
            assert(len(n_args) == 2)
            n1, n2 = [self.process_number(n) for n in n_args]
            n_val = FuncInfo(n_pred, [n1, n2])
            return Num(n_val)
        elif n_pred_lower in ["neg", "sqrt"]:
            assert(len(n_args) == 1)
            n = self.process_number(n_args[0])
            n_val = FuncInfo(n_pred, [n])
            return Num(n_val)
        else:
            raise NotImplementedError(f"[process_number] Unsupporrted number pred: {n_pred}")


    def process_rs(self, rs_info):

        if isinstance(rs_info, str) and rs_info.lower() == "rsarbitrary":
            return Root("arbitrary", list())

        rs_pred_lower = rs_info[0].lower()
        rs_pred = CASE_FIX[rs_pred_lower]
        rs_args = rs_info[1:]

        if rs_pred_lower == "rsneq":
            assert(len(rs_args) == 1)
            p_neq = self.process_point(rs_args[0])
            return Root("neq", [p_neq])
        elif rs_pred_lower == "rsoppsides":
            assert(len(rs_args) == 2)
            opp_p = self.process_point(rs_args[0])
            dividing_line = self.process_line(rs_args[1])
            return Root("oppSides", [opp_p, dividing_line])
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
