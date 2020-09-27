import pdb
import argparse

from instruction import Assert, AssertNDG, Confirm, Sample, Parameterize, Compute
from constraint import Constraint
from parse import parse_sexprs
from cline import Point, Line, Circle
from util import Root


class InstructionReader:
    def __init__(self, lines):
        self.points = list()
        self.instructions = list()
        self.lines = lines

        cmds = parse_sexprs(self.lines)
        for cmd in cmds:
            self.process_command(cmd)

    def process_command(self, cmd):
        pred = cmd[0]
        if pred == "sample":
            self.sample(cmd)
        elif pred == "assert":
            self.add(cmd)
        elif pred == "compute":
            self.compute(cmd)
        elif pred == "confirm":
            self.confirm(cmd)
        elif pred == "param":
            self.param(cmd)
        else:
            pdb.set_trace()
            raise NotImplementedError(f"[InstructionReader.process_command] Command not supported: {pred}")


    def sample(self, cmd):

        ps = [self.process_term(p) for p in cmd[1]]
        assert(all([isinstance(p, Point) and isinstance(p.val, str) for p in ps]))

        method = cmd[2]

        if method in ["triangle", "acuteTri", "equiTri", "polygon"]:
            assert(len(cmd) == 3)
            instr = Sample(ps, method) # No extra args here
            self.instructions.append(instr)
        elif method in ["rightTri", "isoTri", "acuteIsoTri"]:
            assert(len(cmd) == 4)
            args = cmd[3]
            assert(len(args) == 1)
            special_p = self.process_term(args[0])
            assert(isinstance(special_p, Point) and isinstance(special_p.val, str))
            instr = Sample(ps, method, (special_p))
            self.instructions.append(instr)
        else:
            pdb.set_trace()
            raise NotImplementedError(f"[InstructionReader.sample] Sampling method not yet supported: {method}")


    def compute(self, cmd):
        if len(cmd) != 3:
            raise RuntimeError(f"Malformed compute command: {cmd}")

        p = cmd[1]
        computation = self.process_point(cmd[2])
        assert(not isinstance(computation.val, str))
        c_instr = Compute(p, computation)
        self.instructions.append(c_instr)


    # THEN, look over everything, then update point compilatoina nd optimization with Point type
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
        assert(len(cmd) == 3)

        p = self.process_term(cmd[1])
        assert(isinstance(p, Point) and isinstance(p.val, str))

        negate, pred, args = self.process_constraint(cmd[2])
        assert(pred in ["onSeg", "onL", "onC", "onRay"])
        assert(not negate)
        p_instr = Parameterize(p, (pred, args))
        self.instructions.append(p_instr)


    def process_constraint(self, constraint):
        negate = (constraint[0] == "not")
        if negate:
            constraint = constraint[1]

        pred = constraint[0]
        args = constraint[1:]
        args = [self.process_term(t) for t in args]

        ps = [t for t in args if isinstance(t, Point)]
        ls = [t for t in args if isinstance(t, Line)]
        cs = [t for t in args if isinstance(t, Circle)]

        # Validate
        if pred == "cong":
            assert(len(args) == 4)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "onL":
            assert(len(args) == 2)
            assert(isinstance(args[0], Point) and isinstance(args[1], Line))
        elif pred == "onSeg":
            assert(len(args) == 2)
            assert(all([isinstance(t, Point) for t in args]))
        elif pred == "para":
            if len(args) == 2:
                assert(all([isinstance(t, Line) for t in args]))
            elif len(args) == 4:
                assert(all([isinstance(t, Point) for t in args]))
                l1 = Line("connecting", [args[0], args[1]])
                l2 = Line("connecting", [args[2], args[3]])
                args = [l1, l2]
            else:
                raise RuntimeError(f"Invalid para constraint {constraint}")
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
                    raise RuntimeError(f"Term {term} not a point/line/circle")

    def process_point(self, p_info):
        if isinstance(p_info, str):
            return Point(p_info)
        if not isinstance(p_info, tuple):
            raise NotImplementedError(f"[process_point] p_info must be tuple or string")

        p_pred = p_info[0]
        p_args = p_info[1:]
        if p_pred == "interLL":
            assert(len(p_args) == 2)
            l1 = self.process_line(p_args[0])
            l2 = self.process_line(p_args[1])
            p_val = ("interLL", l1, l2)
            return Point(p_val)
        elif p_pred == "incenter":
            assert(len(p_args) == 3)
            ps = [self.process_point(p) for p in p_args]
            p_val = ("incenter", ps)
            return Point(p_val)
        elif p_pred == "interLC":
            assert(len(p_args) == 3)
            l = self.process_line(p_args[0])
            c = self.process_circle(p_args[1])
            rs = self.process_rs(p_args[2])
            p_val = ("interLC", l, c, rs)
            return Point(p_val)
        elif p_pred == "interCC":
            assert(len(p_args) == 3)
            c1 = self.process_circle(p_args[0])
            c2 = self.process_circle(p_args[1])
            rs = self.process_rs(p_args[2])
            p_val = ("interCC", c1, c2, rs)
            return Point(p_val)
        else:
            raise NotImplementedError(f"[process_point] Unrecognized p_pred {p_pred}")

    def process_line(self, l_info):
        l_pred = l_info[0]
        ps = [self.process_point(p) for p in l_info[1:]]
        if l_pred == "line":
            assert(len(ps) == 2)
            return Line("connecting", ps)
        elif l_pred == "perpAt":
            assert(len(ps) == 3)
            return Line("perpAt", ps)
        elif l_pred == "perpBis":
            assert(len(ps) == 2)
            return Line("perpBis", ps)
        else:
            pdb.set_trace()
            return NotImplementedError(f"[process_line] Unsupported line pred: {l_pred}")

    def process_circle(self, c_info):
        c_pred = c_info[0]
        ps = [self.process_point(p) for p in c_info[1:]]
        if c_pred == "circ":
            assert(len(ps) == 3)
            return Circle("c3", ps)
        else:
            pdb.set_trace()
            return NotImplementedError(f"[process_circle] Unsupported circle pred: {c_pred}")

    def process_rs(self, rs_info):
        rs_pred = rs_info[0]
        rs_args = rs_info[1:]
        if rs_pred == "rsNeq":
            assert(len(rs_args) == 1)
            p_neq = self.process_point(rs_info[0])
            return Root("neq", [p_neq])
        else:
            pdb.set_trace()
            return NotImplementedError(f"[process_rs] Unsupported rs pred: {rs_pred}")

if __name__ == "__main__":
    # Get problem to compile
    parser = argparse.ArgumentParser(description='Arguments for compiling a file of instructions to an instruction set')
    parser.add_argument('--problem', '-p', action='store', type=str, help='Name of the file defining the set of constraints')

    args = parser.parse_args()
    lines = open(args.problem, 'r').readlines()

    reader = InstructionReader(lines)
    instructions = reader.instructions
