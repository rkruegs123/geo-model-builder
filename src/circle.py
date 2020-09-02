class Circle:
    def __init__(self, pred, points):
        self.pred = pred
        self.points = points

    def pointsOn(self):
        if self.pred == "coa":
            return [self.points[1]]
        elif self.pred == "c3":
            return self.points
        elif self.pred == "cong":
            return list()
        elif self.pred == "diam":
            return self.points
