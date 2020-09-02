from abc import ABC, abstractmethod

class Cline(ABC):
    def __init__(self, pred, points):
        self.pred = pred
        self.points = points
        super().__init__()

    @abstractmethod
    def pointsOn(self):
        pass

class Circle(Cline):
    def pointsOn(self):
        if self.pred == "coa":
            return [self.points[1]]
        elif self.pred == "c3":
            return self.points
        elif self.pred == "cong":
            return list()
        elif self.pred == "diam":
            return self.points
        else:
            raise RuntimeError("[Circle.pointsOn] Invalid circle pred")

class Line(Cline):
    def pointsOn(self):
        if self.pred == "connecting":
            return self.points
        elif self.pred == "paraAt":
            return [self.points[0]]
        elif self.pred == "perpAt":
            return [self.points[0]]
        elif self.pred == "mediator":
            return list()
        elif self.pred == "iBisector":
            return [self.points[1]]
        elif self.pred == "eBisector":
            return [self.points[1]]
        elif self.pred == "eqOAngle":
            return [self.points[0]]
        else:
            raise RuntimeError("[Line.pointsOn] Invalid line pred")
