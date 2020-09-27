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
        else:
            pdb.set_trace()
            raise NotImplementedError(f"[InstructionReader.process_command] Command not supported: {pred}")


    def sample(self, cmd):
        assert(len(cmd) == 3 or len(cmd) == 4)

        ps = [self.process_term(p) for p in cmd[1]]
        assert(all([isinstance(p.val, str) for p in ps]))

        method = cmd[2]

        if len(cmd) == 4:
            args = cmd[3]

        if method in ["triangle", "acuteTri", "equiTri", "polygon"]:
            instr = Sample(ps, method) # No extra args here
        else:
            pdb.set_trace()
            raise NotImplementedError(f"[InstructionReader.sample] Sampling method not yet supported: {method}")

    def add(self, cmd):
        negate = (cmd[1][0] == "not")
        constraint = cmd[1][1] if negate else cmd[1]
        cons_pred = constraint[0]
        cons_args = constraint[1:]
        cons_args = [self.process_term(t) for t in cons_args]

        instr_cons = Constraint(cons_pred, cons_args, False)
        if negate:
            self.instructions.append(AssertNDG(instr_cons))
        else:
            self.instructions.append(Assert(instr_cons))


    def compute(self, cmd):
        if len(cmd) != 3:
            raise RuntimeError(f"Malformed compute command: {cmd}")

        p = cmd[1]
        computation = self.process_point(cmd[2])
        assert(not isinstance(computation.val, str))
        c_instr = Compute(p, computation)
        self.instructions.append(c_instr)

    def confirm(self, cmd):
        negate = (cmd[1][0] == "not")
        constraint = cmd[1][1] if negate else cmd[1]
        cons_pred = constraint[0]
        cons_args = constraint[1:]
        cons_args = [self.process_term(t) for t in cons_args]

        instr_cons = Constraint(cons_pred, cons_args, negate)
        self.instructions.append(Confirm(instr_cons))

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
