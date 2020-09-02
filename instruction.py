import collections

# TODO: Have one for each IR type? No "Instruction" base class?
Compute = collections.namedtuple("Compute", ["point", "computation"])
Parameterize = collections.namedtuple("Parameterize", ["point", "parameterization"])
Sample = collections.namedtuple("Sample", ["points", "sampler"])
Assert = collections.namedtuple("Assert", ["constraint"])
AssertNDG = collections.namedtuple("AssertNDG", ["constraint"])
Confirm = collections.namedtuple("Confirm", ["constraint"])
