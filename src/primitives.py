from abc import ABC, abstractmethod
import collections
import numbers

from util import FuncInfo



class Primitive(ABC):
    def __init__(self, val):
        self.val = val
        super().__init__()

    def __eq__(self, other):
        if type(self) != type(other):
            # don't attempt to compare against unrelated types
            return NotImplementedError("Must test equality with same types for Primitive")

        return self.val == other.val

    def __hash__(self):
        return hash(self.val)

    @abstractmethod
    def __str__(self):
        pass


class Point(Primitive):
    def __str__(self):
        if isinstance(self.val, str):
            return self.val
        else:
            return f"({self.val[0]} {' '.join([str(v) for v in self.val[1]])})"



class Num(Primitive):
    def __str__(self):
        if isinstance(self.val, numbers.Number):
            return str(self.val)
        else:
            return f"({self.val[0]} {' '.join([str(v) for v in self.val[1]])})"


class Circle(Primitive):

    def __str__(self):
        if isinstance(self.val, str):
            return self.val
        elif isinstance(self.val, FuncInfo):
            pred, args = self.val
            return f"({pred} {' '.join([str(a) for a in args])})"
        else:
            raise RuntimeError("Invalid circle")

class Line(Primitive):

    def __str__(self):
        if isinstance(self.val, str):
            return self.val
        elif isinstance(self.val, FuncInfo):
            pred, args = self.val
            return f"({pred} {' '.join([str(a) for a in args])})"
        else:
            raise RuntimeError("Invalid line")
