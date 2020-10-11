import collections
import pdb
import random
import string


class Root(collections.namedtuple("Root", ["pred", "vars"])):
    def __str__(self):
        return f"(root-{self.pred} {' '.join([str(v) for v in self.vars])})"


Bucket = collections.namedtuple("Bucket", ["points", "assertions"])
FuncInfo = collections.namedtuple("FuncInfo", ["head", "args"])

def is_sample_pred(pred):
    return pred in ["triangle", "polygon"]

def group_pairs(p, ps):
    if len(ps) != 4:
        raise RuntimeError("[group_pairs] Wrong number of points passed to group_pairs")
    a, b, c, d = ps
    if p == a and p not in [b, c, d]:
        return (b, (c, d))
    elif p == b and p not in [a, c, d]:
        return (a, (c, d))
    elif p == c and p not in [a, b, d]:
        return (d, (a, b))
    elif p == d and p not in [a, b, c]:
        return (c, (a, b))
    return (None, None)

def match_in_first_2(p, ps):
    if len(ps) != 4:
        raise RuntimeError("[match_in_first_2] Wrong number of points passed to match_in_first_2")
    x, y, a, b = ps
    if p == x and p not in [y, a, b]:
        return True, (y, a, b)
    if p == y and p not in [x, a, b]:
        return True, (x, a, b)
    return (False, None)

DEFAULTS = {
    "decay_steps": 1e3,
    "decay_rate": 0.7,
    "distinct_prob": 0.5,
    "eps": 1e-3,
    "learning_rate": 1e-1,
    "make_distinct": 1e-2,
    "min_dist": 0.1,
    "n_iterations": 5000,
    "ndg_loss": 1e-3,
    "regularize_points": 1e-6,
    "solver": "tensorflow",
    "n_models": 3,
    "n_tries_per_model": 2,
    "verbosity": 1,
}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
