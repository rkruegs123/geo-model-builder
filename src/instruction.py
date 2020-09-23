import collections
from util import *

# TODO: Instruction base class?

class Parameterize:
    def __init__(self, point, parameterization):
        self.point = point
        self.parameterization = parameterization

    def __str__(self):

        if self.parameterization[0] == "coords":
            param_str = "coords"
        elif isinstance(self.parameterization, collections.abc.Iterable) and type(self.parameterization) != str:
            param_str = ' '.join(str(x) for x in self.parameterization)
        else:
            param_str = str(self.parameterization)

        return "parameterize {p} {p_str}".format(
            p=self.point,
            p_str=param_str
        )

class Compute:
    def __init__(self, point, computation):
        self.point = point
        self.computation = computation

    def __str__(self):
        if isinstance(self.computation, collections.abc.Iterable) and type(self.computation) != str:
            comp_str = ' '.join(str(x) for x in self.computation)
        else:
            comp_str = str(self.computation)
        return "compute {p} ({computation_str})".format(
            p=self.point,
            computation_str=comp_str
        )

class Sample:
    def __init__(self, points, sampler, args=()):
        self.points = points
        self.sampler = sampler
        self.args = args

    def __str__(self):
        return f"sample [{' '.join(self.points)}] {self.sampler} [{' '.join(self.args)}]"

class Confirm:
    def __init__(self, constraint):
        self.constraint = constraint

    def __str__(self):
        return f"confirm ({self.constraint})"

class Assert:
    def __init__(self, constraint):
        self.constraint = constraint

    def __str__(self):
        return f"assert ({self.constraint})"

class AssertNDG:
    def __init__(self, constraint):
        self.constraint = constraint

    def __str__(self):
        return f"assertNDG ({self.constraint})"
