import collections


class Expr(collections.namedtuple("Expr", ["op", "args"])):
    def __add__(self, e):
        return Expr("add", [self, e])

    def __sub__(self, e):
        return Expr("sub", [self, e])

    def __mul__(self, e):
        return Expr("mul", [self, e])

    def __truediv__(self, e):
        return Expr("div", [self, e])

    def __pow__(self, e):
        return Expr("pow", [self, e])

    def __neg__(self):
        return Expr("neg", [self])

def const(x):
    return Expr("const", [x])

class Point(collections.namedtuple("Point", ["x", "y"])):
    def __add__(self, p):
        return Point(self.x + p.x, self.y + p.y)

    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y)

    def smul(self, z):
        return Point(self.x * z, self.y * z)

    def sdiv(self, z):
        return Point(self.x / z, self.y / z)


#####################
## Computational Geometry
####################




def matrix_mul(mat, pt):
    pt1, pt2 = mat
    return Point(x=inner_product(pt1, pt), y=inner_product(pt2,pt))

def inner_product(A, B):
    a1, a2 = A
    b1, b2 = B
    return a1*b1 + a2*b2

def rotation_matrix(theta):
    r1 = Point(x=Expr("cos" [theta]), y=Expr("neg", [Expr("sin", [theta])]))
    r1 = Point(x=Expr("sin" [theta]), y=Expr("cos", [theta]))
    return (r1, r2)

def rotate_counterclockwise(theta, pt):
    return matrix_mul(rotation_matrix(theta), pt)

def rotate_clockwise_90(pt):
    return matrix_mul((Point(x=Expr("const", [0.0]), y=Expr("const", [1.0])), Point(x=Expr("const", [-1.0]),y=Expr("const", [0.0]))), pt)

def rotate_counterclockwise_90(pt):
    return matrix_mul((Point(x=Expr("const", [0.0]), y=Expr("const", [-1.0])), Point(x=Expr("const", [1.0]),y=Expr("const", [0.0]))), pt)


def midp(self, A, B):
    return (A + B).smul(0.5)

def sqdist(A, B):
    t1 = Expr("pow", [Expr("sub", [A.x, B.x]), 2.0])
    t2 = Expr("pow", [Expr("sub", [A.y, B.y]), 2.0])
    return Expr("add", [t1, t2])

def dist(A, B):
    return Expr("pow", [sqdist(A, B), 0.5])
