import collections

# TODO: Instruction base class?

class Parameterize:
    def __init__(self, point, parameterization):
        self.point = point
        self.parameterization = parameterization

    def __str__(self):
        if isinstance(self.parameterization, collections.abc.Iterable):
            param_str = ' '.join(str(x) for x in self.parameterization)
        else:
            param_str = str(self.parameterization)
        return "parameterize {p} {p_str}".format(
            p=self.point,
            p_str=param_str
        )

class Compute:
    def __init__(self, points, computation):
        self.points = points
        self.computation = computation

    def __str__(self):
        if isinstance(self.computation, collections.abc.Iterable):
            comp_str = ' '.join(str(x) for x in self.computation)
        else:
            comp_str = str(self.computation)
        return "compute {ps} ({computation_str})".format(
            ps=self.points,
            computation_str=comp_str
        )

class Sample:
    def __init__(self, points, sampler):
        self.points = points
        self.sampler = sampler

    def __str__(self):
        return f"sample [{' '.join(self.points)}] {self.sampler}"

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
