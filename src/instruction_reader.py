import pdb
import argparse
import math

from instruction import Assert, AssertNDG, Confirm, Sample, Parameterize, Compute
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

        self.problem_type = None

        cmds = parse_sexprs(self.problem_lines)
        for cmd in cmds:
            self.process_command(cmd)

        print("INPUT INSTRUCTIONS:\n{instrs_str}".format(
            instrs_str="\n".join([str(i) for i in self.instructions])))

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
        pred = cmd[0]
        if pred == "sample":
            raise NotImplementedError("Sample is deprecated")
            # self.sample(cmd)
            # self.update_problem_type("instructions")
        elif pred == "assert":
            self.add(cmd)
        elif pred == "compute":
            self.compute(cmd)
            self.update_problem_type("instructions")
        elif pred == "confirm":
            self.confirm(cmd)
        elif pred == "param":
            if isinstance(cmd[1], str):
                self.param(cmd)
            elif isinstance(cmd[1], tuple):
                self.param_special(cmd)
            else:
                raise RuntimeError("Invalid param input type")
            self.update_problem_type("instructions")
        elif pred == "declare-points":
            assert(len(cmd) > 1)
            ps = cmd[1:]
            for p in ps:
                self.register_pt(Point(p))
            self.update_problem_type("compile")
        elif pred == "declare-point":
            assert(len(cmd) == 2)
            p = cmd[1]
            self.register_pt(Point(p))
            self.update_problem_type("compile")
        else:
            raise NotImplementedError(f"[InstructionReader.process_command] Command not supported: {pred}")


    # def sample(self, cmd):
    def param_special(self, cmd):

        assert(len(cmd) == 3)

        ps = [Point(p) for p in cmd[1]]
        for p in ps:
            self.register_pt(p)

        param_method = cmd[2]

        if isinstance(param_method, str):
            assert(param_method in ["triangle", "acuteTri", "equiTri", "polygon"])
            instr = Sample(ps, param_method) # No extra args here
            self.instructions.append(instr)
        elif isinstance(param_method, tuple):
            assert(len(param_method) == 2)
            head, arg = param_method
            assert(head in ["rightTri", "isoTri", "acuteIsoTri"])
            assert(isinstance(arg, str) and Point(arg) in ps)
            special_p = Point(arg) # Not coming in as Point
            instr = Sample(ps, head, (special_p,))
            self.instructions.append(instr)
        else:
            raise RuntimeError("Invalid joint param method")


    def compute(self, cmd):
        assert(len(cmd) == 4)

        obj_name = cmd[1]
        assert(isinstance(obj_name, str))

        obj_type = cmd[2]
        assert(obj_type in ["point", "line", "circle"])

        if obj_type == "point":
            p = Point(obj_name)
            self.register_pt(p)

            computation = self.process_point(cmd[3])
            assert(not isinstance(computation.val, str))

            c_instr = Compute(p, computation)
            self.instructions.append(c_instr)
        elif obj_type == "line":
            l = Line(obj_name)
            self.register_line(l)

            computation = self.process_line(cmd[3])
            assert(not isinstance(computation.val, str))

            c_instr = Compute(l, computation)
            self.instructions.append(c_instr)

        elif obj_type == "circle":
            c = Circle(obj_name)
            self.register_circ(c)

            computation = self.process_circle(cmd[3])
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

        obj_type = cmd[2]
        assert(obj_type in ["point", "line", "circle"])

        if obj_type == "line":
            assert(len(cmd) == 3)
            l = Line(cmd[1])
            self.register_line(l)
            p_instr = Parameterize(l, ("line", None))
            self.instructions.append(p_instr)
        elif obj_type == "circle":
            assert(len(cmd) == 3)
            c = Circle(cmd[1])
            self.register_circ(c)
            p_instr = Parameterize(c, ("circle", None))
            self.instructions.append(p_instr)
        else:
            p = Point(cmd[1])
            self.register_pt(p)

            param_method = "coords"
            if len(cmd) == 4:
                param_method = cmd[3]
            pred, args = self.process_param(param_method)
            p_instr = Parameterize(p, (pred, args))
            self.instructions.append(p_instr)

    def process_param(self, param):
        if param == "coords":
            return "coords", None

        pred = param[0]
        args = param[1:]
        args = [self.process_term(t) for t in args]

        ps = [t for t in args if isinstance(t, Point)]
        ls = [t for t in args if isinstance(t, Line)]
        cs = [t for t in args if isinstance(t, Circle)]

        if pred == "onSeg":
            assert(len(args) == 2)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "onLine":
            assert(len(args) == 1)
            assert(all([isinstance(t, Line) for t in args]))
        elif pred == "onRay":
            assert(len(args) == 2)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "onCirc":
            assert(len(args) == 1)
            assert(all([isinstance(t, Circle) for t in args]))
        elif pred == "inPoly":
            assert(len(args) >= 3)
            assert(all([isinstance(t, Point) for t in args]))
        else:
            raise NotImplementedError(f"[process_param] unrecognized param {param}")
        return pred, args


    def process_constraint(self, constraint):
        assert(isinstance(constraint, tuple))

        negate = (constraint[0] == "not")
        if negate:
            constraint = constraint[1]

        pred = constraint[0]
        args = constraint[1:]
        args = [self.process_term(t) for t in args]

        ps = [t for t in args if isinstance(t, Point)]
        ls = [t for t in args if isinstance(t, Line)]
        cs = [t for t in args if isinstance(t, Circle)]
        ns = [t for t in args if isinstance(t, Num)]

        # Validate
        if pred == "acutes":
            assert(len(args) == 3)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "circumcenter":
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
        elif pred == "eq" or pred == "=":
            pred = "eq"
            assert(len(args) == 2)
            assert(all([isinstance(t, Num) for t in args]))
        elif pred == "eqangle":
            assert(len(args) == 8)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "eqratio":
            assert(len(args) == 8)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "ibisector":
            assert(len(args) == 4)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "interLL":
            assert(len(args) == 5)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "insidePolygon":
            assert(len(args) >= 4)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "midp":
            assert(len(args) == 3)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "onLine":
            assert(len(args) == 2)
            assert(isinstance(args[0], Point) and isinstance(args[1], Line))
        elif pred == "onSeg":
            assert(len(args) == 3)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "onCirc":
            assert(len(args) == 2)
            assert(isinstance(args[0], Point) and isinstance(args[1], Circle))
        elif pred == "para" or pred == "perp":
            if len(args) == 2:
                assert(all([isinstance(t, Line) for t in args]))
            elif len(args) == 4:
                assert(all([isinstance(t, Point) for t in args]))
                '''
                l1 = Line("connecting", [args[0], args[1]])
                l2 = Line("connecting", [args[2], args[3]])
                args = [l1, l2]
                '''
            else:
                raise RuntimeError(f"Invalid para constraint {constraint}")
        elif pred == "polygon":
            assert(len(args) >= 3)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "triangle":
            assert(len(args) == 3)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "tangent":
            assert(len(args) == 2)
            assert(isinstance(args[0], Line) or isinstance(args[1], Circle))
            assert(isinstance(args[1], Circle))
        elif pred == "tangentAt":
            assert(len(args) == 3)
            assert(isinstance(args[0], Point))
            assert(isinstance(args[1], Line) or isinstance(args[1], Circle))
            assert(isinstance(args[2], Circle))
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

    def process_point(self, p_info):
        if isinstance(p_info, str) and not is_number(p_info):
            assert(Point(p_info) in self.points)
            return Point(p_info)
        if not isinstance(p_info, tuple):
            raise NotImplementedError(f"[process_point] p_info must be tuple or string")

        p_pred = p_info[0]
        p_args = p_info[1:]
        if p_pred == "interLL":
            assert(len(p_args) == 2)
            l1 = self.process_line(p_args[0])
            l2 = self.process_line(p_args[1])
            p_val = FuncInfo("interLL", (l1, l2))
            return Point(p_val)
        elif p_pred in ["incenter", "excenter"]:
            assert(len(p_args) == 3)
            ps = [self.process_point(p) for p in p_args]
            p_val = FuncInfo(p_pred, tuple(ps))
            return Point(p_val)
        elif p_pred == "interLC":
            assert(len(p_args) == 3)
            l = self.process_line(p_args[0])
            c = self.process_circle(p_args[1])
            rs = self.process_rs(p_args[2])
            p_val = FuncInfo("interLC", (l, c, rs))
            return Point(p_val)
        elif p_pred == "interCC":
            assert(len(p_args) == 3)
            c1 = self.process_circle(p_args[0])
            c2 = self.process_circle(p_args[1])
            rs = self.process_rs(p_args[2])
            p_val = FuncInfo("interCC", (c1, c2, rs))
            return Point(p_val)
        elif p_pred in ["midp", "midpFrom"]:
            assert(len(p_args) == 2)
            ps = [self.process_point(p) for p in p_args]
            p_val = FuncInfo(p_pred, tuple(ps))
            return Point(p_val)
        elif p_pred in ["orthocenter", "circumcenter", "centroid", "incenter"]:
            assert(len(p_args) == 3)
            ps = [self.process_point(p) for p in p_args]
            p_val = FuncInfo(p_pred, tuple(ps))
            return Point(p_val)
        else:
            raise NotImplementedError(f"[process_point] Unrecognized p_pred {p_pred}")

    def process_line(self, l_info):
        if isinstance(l_info, str) and not is_number(l_info):
            assert(Line(l_info) in self.lines)
            return Line(l_info)
        if not isinstance(l_info, tuple):
            raise NotImplementedError(f"[process_line] l_info must be tuple or string")


        l_pred = l_info[0]
        ps = [self.process_point(p) for p in l_info[1:]]

        l_val = None

        if l_pred == "line":
            assert(len(ps) == 2)
            l_val = FuncInfo("connecting", ps)
        elif l_pred == "perpAt":
            assert(len(ps) == 3)
            l_val = FuncInfo("perpAt", ps)
        elif l_pred == "paraAt":
            assert(len(ps) == 3)
            l_val = FuncInfo("paraAt", ps)
        elif l_pred == "perpBis":
            assert(len(ps) == 2)
            l_val = FuncInfo("perpBis", ps)
        elif l_pred == "ibisector":
            assert(len(ps) == 3)
            l_val = FuncInfo("ibisector", ps)
        elif l_pred == "ebisector":
            assert(len(ps) == 3)
            l_val = FuncInfo("ebisector", ps)

        if l_val is not None:
            self.update_problem_type("instructions")
            return Line(l_val)
        else:
            raise NotImplementedError(f"[process_line] Unsupported line pred: {l_pred}")

    def process_circle(self, c_info):
        if isinstance(c_info, str) and not is_number(c_info):
            assert(Circle(c_info) in self.circles)
            return Circle(c_info)
        if not isinstance(c_info, tuple):
            raise NotImplementedError(f"[process_circle] c_info must be tuple or string")

        c_pred = c_info[0]
        ps = [self.process_point(p) for p in c_info[1:]]
        c_val = None

        if c_pred == "circ":
            assert(len(ps) == 3)
            c_val = FuncInfo("c3", ps)
        elif c_pred == "coa":
            assert(len(ps) == 2)
            c_val = FuncInfo("coa", ps)
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
        elif c_pred == "mixtilinearIncircle":
            assert(len(ps) == 3)
            c_val = FuncInfo("mixtilinearIncircle", ps)

        if c_val is not None:
            self.update_problem_type("instructions")
            return Circle(c_val)
        else:
            raise NotImplementedError(f"[process_circle] Unsupported circle pred: {c_pred}")

    def process_number(self, n_info):
        if isinstance(n_info, str) and n_info.lower() == "pi":
            return Num(math.pi)
        if isinstance(n_info, str) and is_number(n_info):
            return Num(float(n_info))
        if not isinstance(n_info, tuple):
            raise NotImplementedError(f"[process_number] n_info must be tuple or string")

        n_pred = n_info[0]
        n_args = n_info[1:]
        if n_pred == "dist":
            assert(len(n_args) == 2)
            p1 = self.process_point(n_args[0])
            p2 = self.process_point(n_args[1])
            n_val = FuncInfo("dist", [p1, p2])
            return Num(n_val)
        elif n_pred == "uangle":
            assert(len(n_args) == 3)
            p1, p2, p3 = [self.process_point(p) for p in n_args]
            n_val = FuncInfo("uangle", [p1, p2, p3])
            return Num(n_val)
        elif n_pred == "radius":
            assert(len(n_args) == 1)
            circ = self.process_circle(n_args[0])
            n_val = FuncInfo("radius", [circ])
            return Num(n_val)
        elif n_pred in ["div", "add", "sub", "mul", "pow"]:
            assert(len(n_args) == 2)
            n1, n2 = [self.process_number(n) for n in n_args]
            n_val = FuncInfo(n_pred, [n1, n2])
            return Num(n_val)
        else:
            raise NotImplementedError(f"[process_number] Unsupporrted number pred: {n_pred}")


    def process_rs(self, rs_info):
        rs_pred = rs_info[0]
        rs_args = rs_info[1:]
        if rs_pred == "rsNeq":
            assert(len(rs_args) == 1)
            p_neq = self.process_point(rs_args[0])
            return Root("neq", [p_neq])
        elif rs_pred == "rsOppSides":
            assert(len(rs_args) == 2)
            opp_p = self.process_point(rs_args[0])
            dividing_line = self.process_line(rs_args[1])
            return Root("oppSides", [opp_p, dividing_line])
        elif rs_info == "rsArbitrary":
            return Root("arbitrary", list())
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
