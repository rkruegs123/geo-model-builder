class Constraint:
    def __init__(self, pred, args, negate):
        self.pred = pred
        self.args = args
        self.negate = negate

    def ndgs(self):
        if (self.pred == "ibisector" or self.pred == "ebisector") and not self.negate:
            return [Constraint("coll", self.args[1:], False)]
        else:
            return list()

    def orders(self):
        if self.pred == "ibisector" and not self.negate:
            x, b, a, c = self.args[0], self.args[1], self.args[2], self.args[3]
            c1 = Constraint("sameSide", [x, b, a, c], False)
            c2 = Constraint("sameSide", [x, c, a, b], False)
            return [c1, c2]
        else:
            return list()


    def __str__(self):
        c_str = ' '.join([self.pred] + [str(a) for a in self.args])
        if self.negate:
            return (f"not ({c_str})")
        else:
            return c_str

def constraint_ndgs(c):
    if c.pred == "ibisector" or c.pred == "ebisector":
        return [Constraint("coll", c.args, False)]
    else:
        return list()

def constraint_orders(c):
    if c.pred == "ibisector":
        x, b, a, c = c.args[0], c.args[1], c.args[2], c.args[3]
        c1 = Constraint("sameSide", [x, b, a, c], False)
        c2 = Constraint("sameSide", [x, c, a, b], False)
        return [c1, c2]
    else:
        return list()
