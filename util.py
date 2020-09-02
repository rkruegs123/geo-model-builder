import collections

Root = collections.namedtuple("Root", ["pred", "vars"])
Bucket = collections.namedtuple("Bucket", ["points", "assertions"])

def is_sample_pred(pred):
    return pred in ["triangle", "polygon"]
