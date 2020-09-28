import sexpdata
import pdb
import argparse

from constraint import Constraint
from util import *
from compile_state import CompileState
from instruction import Assert, AssertNDG, Confirm, Sample
from parse import parse_sexprs
from cline import Point

class PointCompiler:
    def __init__(self, lines):
        self.points = list()
        self.constraints = list()
        self.goals = list()
        self.lines = lines

        cmds = parse_sexprs(self.lines)
        for cmd in cmds:
            self.process_command(cmd)

    def process_command(self, cmd):
        head = cmd[0]
        if head == "declare-points":
            if self.points:
                raise RuntimeError("Duplicate declaration of points")
            self.points = [Point(p) for p in cmd[1:]]
        elif head == "declare-point":
            if len(cmd) != 2:
                raise RuntimeError(f"Mal-formed declare-point cmd: {cmd}")
            p = Point(cmd[1])
            if p in self.points:
                raise RuntimeError(f"Duplicate point encountered: {p}")
            self.points.append(p)
        else:
            term = cmd[1]
            if not isinstance(term, tuple):
                raise RuntimeError(f"Malformed command: {cmd}")
            negate = (term[0] == 'not')
            if negate:
                term = term[1]
            pred = term[0]
            ps = [Point(p) for p in list(term[1:])]
            constraint = Constraint(pred=pred, args=ps, negate=negate)
            if head == "assert":
                self.constraints.append(constraint)
            elif head == "prove":
                self.goals.append(constraint)
            else:
                raise RuntimeError(f"Unrecognized command: {cmd}")


    def preprocess(self):
        sample_points = [p for c in self.constraints for p in c.args if is_sample_pred(c.pred)]
        cs_with_sampled_points = [c for c in self.constraints if not c.negate and set(c.args).issubset(set(sample_points))]
        self.sample_bucket = Bucket(points=sample_points, assertions=cs_with_sampled_points)

        solve_points = [p for p in self.points if p not in sample_points] # maintain order
        cs_to_solve = [c for c in self.constraints if not set(c.args).issubset(set(sample_points)) and not c.negate]
        self.solve_bucket = Bucket(points=solve_points, assertions=cs_to_solve)

        self.ndgs = [Constraint(c.pred, c.args, False) for c in self.constraints if c.negate]


    def sample_bucket_2_instructions(self):
        # Get sample instructions
        sample_instructions = list()
        sample_cs = [c for c in self.sample_bucket.assertions if is_sample_pred(c.pred)]
        aux_cs = [c for c in self.sample_bucket.assertions if not is_sample_pred(c.pred)]

        if aux_cs and not sample_cs:
            raise RuntimeException("Mishandled sampling constraints")

        if not sample_cs:
            return sample_instructions
        elif len(sample_cs) > 1:
            pdb.set_trace()
            raise RuntimeException("Unexpected sampling")

        sampler = sample_cs[0]

        if sampler.pred == "triangle":  # We know len(sample_cs) == 1

            tri_points = sampler.args
            acute = any(c.pred == "acutes" and set(c.args) == set(tri_points) for c in aux_cs)
            iso_points = list(set([collections.Counter(c.args).most_common(1)[0][0] for c in aux_cs if c.pred == "cong"]))
            right_points = list(set([collections.Counter(c.args).most_common(1)[0][0] for c in aux_cs if c.pred == "perp"]))

            if not aux_cs:
                sample_instructions.append(Sample(tri_points, "triangle"))
            elif len(aux_cs) == 1 and acute:
                sample_instructions.append(Sample(tri_points, "acuteTri"))
            elif len(aux_cs) == 2 and acute and len(iso_points) == 1:
                sample_instructions.append(Sample(tri_points, "acuteIsoTri", [iso_points[0]]))
            elif len(aux_cs) == 1 and len(iso_points) == 1:
                sample_instructions.append(Sample(tri_points, "isoTri", [iso_points[0]]))
            elif len(aux_cs) == 2 and len(iso_points) == 2:
                sample_instructions.append(Sample(tri_points, "equiTri"))
            elif len(aux_cs) == 1 and len(right_points) == 1:
                sample_instructions.append(Sample(tri_points, "rightTri", [right_points[0]]))
            else:
                pdb.set_trace()
                raise RuntimeError("Unhandled triangle sampling")
        elif sampler.pred == "polygon":
            poly_points = sampler.args

            if not aux_cs:
                sample_instructions.append(Sample(poly_points, "polygon"))
            else:
                sample_instructions.append(Sample(poly_points, "polygon"))
                sample_instructions += [Assert(c) for c in aux_cs]
        else:
            raise RuntimeError("Mishandled sampling")

        return sample_instructions


    def validate(self):
        all_bucketed_points = self.sample_bucket.points + self.solve_bucket.points

        for c in self.solve_bucket.assertions:
            for p in (c.args):
                if p not in all_bucketed_points:
                    raise RuntimeException("unexpected point " ++ str(p))
        return

    def solve_bucket_2_instructions(self):

        self.validate()

        solve_compiler = CompileState(self.sample_bucket, self.solve_bucket)
        solve_compiler.solve()

        return solve_compiler.solve_instructions

    def compile(self):
        self.preprocess()
        print(self)

        self.instructions = list()

        sample_instructions = self.sample_bucket_2_instructions()
        self.instructions += sample_instructions

        solve_instructions = self.solve_bucket_2_instructions()
        self.instructions += solve_instructions

        self.instructions += [AssertNDG(c) for c in self.ndgs]
        self.instructions += [Confirm(c) for c in self.goals]

        instructions_str = "\nINSTRUCTIONS:\n{header}\n{i_strs}".format(
            header="-" * 13,
            i_strs = '\n'.join([str(i) for i in self.instructions])
        )
        print(instructions_str)

    def __str__(self):
        return '\nPOINTWISE PROBLEM:\n{header}\n\nPoints: {pts}\nConstraints:\n\t{cs}\nGoals:\n\t{gs}\n'.format(
            header='-' * 9,
            pts=' '.join([str(p) for p in self.points]),
            cs='\n\t'.join([str(c) for c in self.constraints]),
            gs='\n\t'.join([str(g) for g in self.goals])
    )

if __name__ == "__main__":
    # Get problem to compile
    parser = argparse.ArgumentParser(description='Arguments for compiling a problem in terms of points to an instruction set')
    parser.add_argument('--problem', '-p', action='store', type=str, help='Name of the file defining the set of constraints')

    args = parser.parse_args()
    lines = open(args.problem, 'r').readlines()

    compiler = PointCompiler(lines)
    compiler.compile()
    instructions = compiler.instructions
