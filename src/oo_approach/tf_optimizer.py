import tensorflow.compat.v1 as tf
import pdb
import collections
import random

from oo_approach.optimizer import Optimizer

class TfPoint(collections.namedtuple("TfPoint", ["x", "y"])):
    def __add__(self, p):  return TfPoint(self.x + p.x, self.y + p.y)
    def __sub__(self, p):  return TfPoint(self.x - p.x, self.y - p.y)
    def sdiv(self, z):     return TfPoint(self.x / z, self.y / z)
    def smul(self, z):     return TfPoint(self.x * z, self.y * z)
    def to_tf(self):       return tf.cast([self.x, self.y], dtype=tf.float64)
    def norm(self):        return tf.norm(self.to_tf(), ord=2)
    def normalize(self):   return self.sdiv(self.norm())
    def has_nan(self):     return tf.logical_or(tf.math.is_nan(self.x), tf.math.is_nan(self.y))
    def __str__(self):     return "(coords %f %f)" % (self.x, self.y)

class TfOptimizer(Optimizer):

    def __init__(self, instructions, opts, graph):
        tfcfg = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
        self.sess = tf.Session(graph=graph, config=tfcfg)

        super().__init__(instructions, opts)

    def get_point(self, x, y):
        return TfPoint(x, y)

    def mkvar(self, name, shape=[], lo=-1.0, hi=1.0, trainable=False):
        init = tf.random_uniform_initializer(minval=lo, maxval=hi)
        return tf.compat.v1.get_variable(name=name, shape=shape, dtype=tf.float64, initializer=init, trainable=trainable)

    #####################
    ## Math Utilities
    ####################
    def addV(self, x, y):
        return x + y

    def subV(self, x, y):
        return x - y

    def negV(self, x):
        return -x

    def sumVs(self, xs):
        return tf.reduce_sum(xs)

    def mulV(self, x, y):
        return x * y

    def divV(self, x, y):
        return x / y

    def powV(self, x, y):
        return x ** y

    def sinV(self, x):
        return tf.math.sin(x)

    def cosV(self, x):
        return tf.math.cos(x)

    def acosV(self, x):
        return tf.math.acos(x)

    def tanhV(self, x):
        return tf.nn.tanh(x)

    def constV(self, x):
        return tf.constant(x, dtype=tf.float64)


    #####################
    ## Tensorflow Utilities
    ####################

    def mk_zero(self, err):
        res = tf.reduce_mean(err**2)
        tf.check_numerics(res, message="mk_zero")
        return res

    def register_pt(self, p, P):
        assert(p not in self.name2pt)
        Px = tf.debugging.check_numerics(P.x, message=str(p))
        Py = tf.debugging.check_numerics(P.y, message=str(p))
        self.name2pt[p] = self.get_point(Px, Py)

    def register_loss(self, key, val, weight=1.0):
        assert(key not in self.losses)
        # TF has a bug that causes nans when differentiating something exactly 0
        self.losses[key] = weight * self.mk_zero(val + 1e-6 * (random.random() / 2))

    #####################
    ## Sample
    ####################

    '''
    def sample_uniform(self, ps):
        [p] = ps
        P   = self.get_point(x=self.uvar(p+"x"), y=self.uvar(p+"y"))
        self.register_pt(p, P)
    '''

    #####################
    ## Core
    ####################

    def run(self, x):
        return self.sess.run(x)

    def solve(self):
        if self.has_loss:
            raise NotImplementedError("[tf_optimizer.solve] Cannot solve with loss")

        assignments = list()
        for _ in range(self.opts.n_tries):
            if not self.has_loss:
                self.run(tf.compat.v1.global_variables_initializer())
                assignment = self.run(self.name2pt)
                assignments.append(assignment)
        return assignments



# try sample polygon (4, then 6 points)
