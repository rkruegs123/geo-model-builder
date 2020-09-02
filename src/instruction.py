import collections

# TODO: Instruction base class?

class Parameterize:
    def __init__(self, point, parameterization):
        self.point = point
        self.parameterization = parameterization

    def __str__(self):
        return f"parameterize {self.point} {self.parameterization}"

class Compute:
    def __init__(self, points, computation):
        self.points = points
        self.computation = computation

    def __str__(self):
        return f"compute {self.points} {self.computation}"

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
