import sexpdata
import pdb

from constraint import Constraint
from util import *
from compile_state import CompileState
from instruction import Assert, AssertNDG, Confirm, Sample
from parse import parse_sexprs

class PointCompiler:
    def __init__(self, filename):
        self.points = list()
        self.constraints = list()
        self.goals = list()
        self.filename = filename

        cmds = parse_sexprs(self.filename)
        for cmd in cmds:
            self.process_command(cmd)

        '''
        for l in open(filename).readlines():
            stripped_l = l.strip()
            if stripped_l and l[0] != ';':
                line_info = sexpdata.loads(stripped_l, true=None)
                if not len(line_info):
                    raise RuntimeError("Empty s-expressions encountered")

                cmd = str(line_info[0]._val)
                if cmd == "declare-points":
                    if self.points:
                        raise RuntimeError("Duplicate declaration of points")
                    if not all(isinstance(p, sexpdata.Symbol) for p in line_info[1:]):
                        raise RuntimeError("Unrecognized load type from sexpdata")
                    self.points = [p._val for p in line_info[1:]]
                elif cmd == "declare-point":
                    if len(line_info) != 2:
                        raise RuntimeError("Mal-formed declare-point")
                    if not isinstance(line_info[1], sexpdata.Symbol):
                        raise RuntimeError("Unrecognized load type from sexpdata")
                    p = line_info[1]._val
                    if p in self.points:
                        raise RuntimeError(f"Duplicate point encountered: {p}")
                    self.points.append(p)
                else:
                    # FIXME: This check won't handle negations
                    # if not all(isinstance(x, sexpdata.Symbol) for x in line_info[1]):
                        # raise RuntimeError("Unrecognized load type from sexpdata")

                    negate = False
                    if line_info[1][0]._val == "not":
                        negate = True
                        pred, args = line_info[1][1][0]._val, [x._val for x in line_info[1][1][1:]]
                    else:
                        pred, args = line_info[1][0]._val, [x._val for x in line_info[1][1:]]
                    if cmd == "assert":
                        self.constraints.append(Constraint(pred=pred, points=args, negate=negate))
                    elif cmd == "prove":
                        self.goals.append(Constraint(pred=pred, points=args, negate=negate))
                    else:
                        raise RuntimeError("Unrecognized command")
        '''

    def process_command(self, cmd):
        head = cmd[0]
        if head == "declare-points":
            if self.points:
                raise RuntimeError("Duplicate declaration of points")
            self.points = list(cmd[1:])
        elif head == "declare-point":
            if len(cmd) != 2:
                raise RuntimeError(f"Mal-formed declare-point cmd: {cmd}")
            p = cmd[1]
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
            ps = list(term[1:])
            constraint = Constraint(pred=pred, points=ps, negate=negate)
            if head == "assert":
                self.constraints.append(constraint)
            elif head == "prove":
                self.goals.append(constraint)
            else:
                raise RuntimeError(f"Unrecognized command: {cmd}")





    def preprocess(self):
        sample_points = [p for c in self.constraints for p in c.points if is_sample_pred(c.pred)]
        cs_with_sampled_points = [c for c in self.constraints if not c.negate and set(c.points).issubset(set(sample_points))]
        self.sample_bucket = Bucket(points=sample_points, assertions=cs_with_sampled_points)

        solve_points = [p for p in self.points if p not in sample_points] # maintain order
        cs_to_solve = [c for c in self.constraints if not set(c.points).issubset(set(sample_points)) and not c.negate]
        self.solve_bucket = Bucket(points=solve_points, assertions=cs_to_solve)

        self.ndgs = [Constraint(c.pred, c.points, False) for c in self.constraints if c.negate]


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

            tri_points = sampler.points
            acute = any(c.pred == "acutes" and set(c.points) == set(tri_points) for c in aux_cs)
            iso_points = list(set([collections.Counter(c.points).most_common(1)[0] for c in aux_cs if c.pred == "cong"]))
            right_points = list(set([collections.Counter(c.points).most_common(1)[0] for c in aux_cs if c.pred == "perp"]))

            if not aux_cs:
                sample_instructions.append(Sample(tri_points, "triangle"))
            elif len(aux_cs) == 1 and acute:
                sample_instructions.append(Sample(tri_points, "acuteTri"))
            elif len(aux_cs) == 1 and iso_points:
                sample_instructions.append(Sample(tri_points, "isoTri", (iso_points[0])))
            elif len(aux_cs) == 2 and acute and iso_points:
                sample_instructions.append(Sample(tri_points, "acuteIsoTri", (iso_points[0])))
            elif len(aux_cs) == 2 and len(iso_points) == 2:
                sample_instructions.append(Sample(tri_points, "equiTri"))
            elif len(aux_cs) == 1 and lenright_points:
                sample_instructions.append(Sample(tri_points, "rightTri", (right_points[0])))
            else:
                pdb.set_trace()
                raise RuntimeError("Unhandled triangle sampling")
        elif sampler.pred == "polygon":
            poly_points = sampler.points

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
            for p in (c.points):
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
        return '\nPOINTWISE PROBLEM: {f}\n{header}\n\nPoints: {pts}\nConstraints:\n\t{cs}\nGoals:\n\t{gs}\n'.format(
            f=self.filename,
            header='-' * (9 + len(self.filename)),
            pts=' '.join(self.points),
            cs='\n\t'.join([str(c) for c in self.constraints]),
            gs='\n\t'.join([str(g) for g in self.goals])
    )