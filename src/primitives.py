"""
Copyright (c) 2020 Ryan Krueger. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Ryan Krueger, Jesse Michael Han, Daniel Selsam
"""

from abc import ABC, abstractmethod
import collections
import numbers
import pdb

from util import FuncInfo



class Primitive(ABC):
    def __init__(self, val):
        self.val = val
        super().__init__()

    def __eq__(self, other):
        if type(self) != type(other):
            return False
            # # don't attempt to compare against unrelated types
            # return NotImplementedError("Must test equality with same types for Primitive")

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

    def pointsOn(self):
        pred, points = self.val
        if pred == "coa":
            return [points[1]]
        elif pred == "c3":
            return points
        elif pred == "cong":
            return list()
        elif pred == "diam":
            return points
        else:
            raise RuntimeError("[Circle.pointsOn] Invalid circle pred")

    def __str__(self):
        if isinstance(self.val, str):
            return self.val
        elif isinstance(self.val, FuncInfo):
            pred, args = self.val
            return f"({pred} {' '.join([str(a) for a in args])})"
        else:
            raise RuntimeError("Invalid circle")

class Line(Primitive):

    def pointsOn(self):
        pred, points = self.val
        if pred == "connecting":
            return points
        elif pred == "paraAt":
            return [points[0]]
        elif pred == "perpAt":
            return [points[0]]
        elif pred == "mediator":
            return list()
        elif pred == "ibisector":
            return [points[1]]
        elif pred == "ebisector":
            return [points[1]]
        elif pred == "eqoangle":
            return [points[0]]
        else:
            raise RuntimeError("[Line.pointsOn] Invalid line pred")

    def __str__(self):
        if isinstance(self.val, str):
            return self.val
        elif isinstance(self.val, FuncInfo):
            pred, args = self.val
            return f"({pred} {' '.join([str(a) for a in args])})"
        else:
            raise RuntimeError("Invalid line")
