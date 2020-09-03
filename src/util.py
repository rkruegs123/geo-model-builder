import collections

Root = collections.namedtuple("Root", ["pred", "vars"])
Bucket = collections.namedtuple("Bucket", ["points", "assertions"])

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
