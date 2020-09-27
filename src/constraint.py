class Constraint:
    def __init__(self, pred, points, negate):
        self.pred = pred
        self.points = points
        self.negate = negate

    def ndgs(self):
        if (self.pred == "ibisector" or self.pred == "ebisector") and not self.negate:
            return [Constraint("coll", self.points[1:], False)]
        else:
            return list()

    def orders(self):
        if self.pred == "ibisector" and not self.negate:
            x, b, a, c = self.points[0], self.points[1], self.points[2], self.points[3]
            c1 = Constraint("sameSide", [x, b, a, c], False)
            c2 = Constraint("sameSide", [x, c, a, b], False)
            return [c1, c2]
        else:
            return list()


    def __str__(self):
        c_str = ' '.join([self.pred] + [str(p) for p in self.points])
        if self.negate:
            return (f"not ({c_str})")
        else:
            return c_str

def constraint_ndgs(c):
    if c.pred == "ibisector" or c.pred == "ebisector":
        return [Constraint("coll", c.points, False)]
    else:
        return list()

def constraint_orders(c):
    if c.pred == "ibisector":
        x, b, a, c = c.points[0], c.points[1], c.points[2], c.points[3]
        c1 = Constraint("sameSide", [x, b, a, c], False)
        c2 = Constraint("sameSide", [x, c, a, b], False)
        return [c1, c2]
    else:
        return list()
