import pdb
import argparse

from instruction import Assert, AssertNDG, Confirm, Sample, Parameterize, Compute
from constraint import Constraint
from parse import parse_sexprs

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
        else:
            pdb.set_trace()
            raise NotImplementedError(f"[InstructionReader.process_command] Command not supported: {pred}")


    def sample(self, cmd):
        ps = cmd[1]
        method = cmd[2]
        if len(cmd) > 3:
            args = cmd[3]

        if method == "acuteTri":
            instr = Sample(ps, method, list())
            self.instructions.append(instr)
        else:
            pdb.set_trace()
            raise NotImplementedError(f"[InstructionReader.sample] Sampling method not yet supported: {method}")

    def add(self, cmd):
        negate = (cmd[1][0] == "not")
        constraint = cmd[1][1] if negate else cmd[1]
        cons_pred = constraint[0]
        cons_args = constraint[1:]
        if all([isinstance(arg, str) for arg in cons_args]):
            instr_cons = Constraint(cons_pred, cons_args, False)
            if negate:
                self.instructions.append(AssertNDG(instr_cons))
            else:
                self.instructions.append(Assert(instr_cons))
        else:
            # Note that when we do, we should be keeping track of the points
            pdb.set_trace()
            raise NotImplementedError(f"[add] Do not yet support non-point arguments")

    def compute(self, cmd):
        if len(cmd) != 3:
            raise RuntimeError(f"Malformed compute command: {cmd}")

        p = cmd[1]
        c_method = cmd[2][0]
        c_args = cmd[2][1:]

        if c_method == "incenter":
            c_instr = Compute(p, ("incenter", c_args))
            self.instructions.append(c_instr)
        else:
            pdb.set_trace()
            raise NotImplementedError(f"[compute] Do not yet support method {c_method}")

if __name__ == "__main__":
    # Get problem to compile
    parser = argparse.ArgumentParser(description='Arguments for compiling a file of instructions to an instruction set')
    parser.add_argument('--problem', '-p', action='store', type=str, help='Name of the file defining the set of constraints')

    args = parser.parse_args()
    lines = open(args.problem, 'r').readlines()

    reader = InstructionReader(lines)
    instructions = reader.instructions
