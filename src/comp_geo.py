import collections
import numbers
import pdb


class Expr(collections.namedtuple("Expr", ["op", "args"])):
    def __add__(self, e):
        return Expr("add", [self, self.preprocess_expr(e)])

    def __sub__(self, e):
        return Expr("sub", [self, self.preprocess_expr(e)])

    def __mul__(self, e):
        return Expr("mul", [self, self.preprocess_expr(e)])

    def __truediv__(self, e):
        return Expr("div", [self, self.preprocess_expr(e)])

    def __pow__(self, e):
        return Expr("pow", [self, self.preprocess_expr(e)])

    def __neg__(self):
        return Expr("neg", [self])

    def preprocess_expr(self, e):
        if isinstance(e, numbers.Number):
            return const(e)
        else:
            return e

# NOTE: The logic for dealing with consts in tf will be something like:
# if const then tf.const, else process_expr (and don't use tf.const)
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
    r1 = Point(x=Expr("cos", [theta]), y=-Expr("sin", [theta]))
    r2 = Point(x=Expr("sin", [theta]), y=Expr("cos", [theta]))
    return (r1, r2)

def rotate_counterclockwise(theta, pt):
    return matrix_mul(rotation_matrix(theta), pt)

def rotate_clockwise_90(pt):
    return matrix_mul((Point(x=const(0.0), y=const(1.0)), Point(x=const(-1.0), y=const(0.0))), pt)

def rotate_counterclockwise_90(pt):
    return matrix_mul((Point(x=const(0.0), y=const(-1.0)), Point(x=const(1.0), y=const(0.0))), pt)

def midp(A, B):
    return (A + B).smul(0.5)

def sqdist(A, B):
    return (A.x - B.x)**2 + (A.y - B.y)**2

def dist(A, B):
    return sqdist(A, B) ** const(0.5)

def side_lengths(A, B, C):
    return dist(B, C), dist(C, A), dist(A, B)

def angle(A, B, C):
    a, b, c = side_lengths(A, B, C)
    return Expr("acos", [(a**2 + c**2 - b**2) / (const(2) * a * c)])
