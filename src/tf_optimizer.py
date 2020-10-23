import tensorflow.compat.v1 as tf
import pdb
import collections
import random
import itertools
from tqdm import tqdm
import os
import glob

from optimizer import Optimizer, LineSF, CircleNF
from diagram import Diagram
from util import get_random_string

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

    def __init__(self, instructions, opts, unnamed_points, unnamed_lines, unnamed_circles, segments, seg_colors, graph):
        # tfcfg = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1, device_count={"CPU": 3})
        tfcfg = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
        self.sess = tf.Session(graph=graph, config=tfcfg)

        super().__init__(instructions, opts, unnamed_points, unnamed_lines, unnamed_circles, segments, seg_colors)

    def get_point(self, x, y):
        return TfPoint(x, y)

    def simplify(self, p, method="all"):
        return p

    def mkvar(self, name, shape=[], lo=-1.0, hi=1.0, trainable=None):
        init = tf.random_uniform_initializer(minval=lo, maxval=hi)
        return tf.compat.v1.get_variable(name=name, shape=shape, dtype=tf.float64, initializer=init, trainable=trainable)

    def mk_normal_var(self, name, shape=[], mean=0.0, std=1.0, trainable=None):
        init = tf.random_normal_initializer(mean=mean, stddev=std)
        return tf.compat.v1.get_variable(name=name, shape=shape, dtype=tf.float64, initializer=init, trainable=trainable)

    #####################
    ## Math Utilities
    ####################
    def sum(self, xs):
        return tf.reduce_sum(xs)

    def sqrt(self, x):
        return tf.math.sqrt(x)

    def sin(self, x):
        return tf.math.sin(x)

    def cos(self, x):
        return tf.math.cos(x)

    def asin(self, x):
        return tf.math.asin(x)

    def acos(self, x):
        return tf.math.acos(x)

    def tanh(self, x):
        return tf.nn.tanh(x)

    def atan2(self, x, y):
        return tf.math.atan2(x, y)

    def sigmoid(self, x):
        return tf.nn.sigmoid(x)

    def const(self, x):
        return tf.constant(x, dtype=tf.float64)

    def max(self, x, y):
        return tf.maximum(x, y)

    def min(self, x, y):
        return tf.minimum(x, y)

    def cond(self, cond, t_lam, f_lam):
        return tf.cond(cond, t_lam, f_lam)

    def lt(self, x, y):
        return tf.less(x, y)

    def lte(self, x, y):
        return tf.less_equal(x, y)

    def gt(self, x, y):
        return tf.greater(x, y)

    def gte(self, x, y):
        return tf.greater_equal(x, y)

    def eq(self, x, y):
        return tf.math.equal(x, y)

    def logical_or(self, x, y):
        return tf.logical_or(x, y)

    def abs(self, x):
        return tf.math.abs(x)

    def exp(self, x):
        return tf.math.exp(x)

    #####################
    ## Tensorflow Utilities
    ####################

    def mk_non_zero(self, err):
        res = tf.reduce_mean(tf.exp(- (err ** 2) * 20))
        tf.check_numerics(res, message="mk_non_zero")
        return res

    def mk_zero(self, err):
        res = tf.reduce_mean(err**2)
        tf.check_numerics(res, message="mk_zero")
        return res

    def register_pt(self, p, P, save_name=True):
        if save_name:
            assert(isinstance(p.val, str))
            assert(p not in self.name2pt)

        Px = tf.debugging.check_numerics(P.x, message=str(p))
        Py = tf.debugging.check_numerics(P.y, message=str(p))
        P_checked = self.get_point(Px, Py)
        self.all_points.append(P_checked)
        if save_name:
            self.name2pt[p] = P_checked
        return P_checked

    def register_line(self, l, L):
        assert(l not in self.name2line)
        assert(isinstance(l.val, str))
        # FIXME: Check numerics
        self.name2line[l] = L
        return L

    def register_circ(self, c, C):
        assert(c not in self.name2circ)
        assert(isinstance(c.val, str))
        r = tf.debugging.check_numerics(C.radius, message=str(c))
        C_checked = CircleNF(center=C.center, radius=r)
        self.name2circ[c] = C_checked
        return C_checked


    def register_loss(self, key, val, weight=1.0, requires_train=True):
        assert(key not in self.losses)
        # TF has a bug that causes nans when differentiating something exactly 0
        self.losses[key] = weight * self.mk_zero(val + 1e-6 * (random.random() / 2))
        if requires_train:
            self.has_loss = True

    def register_ndg(self, key, val, weight=1.0):
        assert(key not in self.ndgs)
        err = weight * self.mk_non_zero(val)
        self.ndgs[key] = err

        self.register_loss(key, err, weight)
        # if self.opts['ndg_loss'] > 0:
            # self.register_loss(key, err, self.opts['ndg_loss'])


    def register_goal(self, key, val, negate):
        assert(key not in self.goals)
        if negate:
            self.goals[key] = self.mk_non_zero(val)
        else:
            self.goals[key] = self.mk_zero(val)

    def regularize_points(self):
        norms = tf.cast([p.norm() for p in self.name2pt.values()], dtype=tf.float64)
        self.register_loss("points", tf.reduce_mean(norms), self.opts['regularize_points'])

    def make_points_distinct(self):
        if random.random() < self.opts['distinct_prob']:
            distincts = tf.cast([self.dist(A, B) for A, B in itertools.combinations(self.name2pt.values(), 2)], tf.float64)
            dloss     = tf.reduce_mean(self.mk_non_zero(distincts))
            self.register_loss("distinct", dloss, self.opts['make_distinct'])

    def freeze(self):
        opts = self.opts
        self.regularize_points()
        self.make_points_distinct()
        self.loss = sum(self.losses.values())
        self.global_step = tf.train.get_or_create_global_step()
        self.learning_rate = tf.train.exponential_decay(
            global_step=self.global_step,
            learning_rate=opts['learning_rate'],
            decay_steps=opts['decay_steps'],
            decay_rate=opts['decay_rate'],
            staircase=False)
        optimizer         = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
        gs, vs            = zip(*optimizer.compute_gradients(self.loss))
        self.apply_grads  = optimizer.apply_gradients(zip(gs, vs), name='apply_gradients', global_step=self.global_step)
        self.reset_step   = tf.assign(self.global_step, 0)
        self.gen_inits()

    def print_losses(self):
        print("======== Print losses ==========")
        print("-- Losses --")
        for k, x in self.run(self.losses).items(): print("  %-50s %.10f" % (k, x))
        print("-- Goals --")
        for k, x in self.run(self.goals).items(): print("  %-50s %.10f" % (k, x))
        print("-- NDGs --")
        for k, x in self.run(self.ndgs).items(): print("  %-50s %.10f" % (k, x))
        print("================================")


    def gen_inits(self):

        if not os.path.exists('.checkpoints'):
            os.makedirs('.checkpoints')

        # delete old checkpoints
        ckpt_list = glob.glob('.checkpoints/*')
        for ckpt_file in ckpt_list:
            os.remove(ckpt_file)

        n_inits = self.n_inits

        init_map = dict() # maps inits to losses
        saver = tf.train.Saver(max_to_keep=None)

        self.global_init = tf.compat.v1.global_variables_initializer()

        n_inits_iter = range(n_inits) if self.verbosity < 0 else tqdm(range(n_inits), desc="Sampling initializations...")

        for _ in n_inits_iter:
            self.sess.run(self.global_init)
            # self.sess.run(tf.compat.v1.global_variables_initializer())
            init_loss = self.sess.run(self.loss)
            init_name = f".checkpoints/{get_random_string(8)}"
            saver.save(self.sess, init_name)
            init_map[init_name] = init_loss

        self.sorted_inits = sorted(init_map.items(), key=lambda x: x[1])


    def remove_inits(self):
        # remove init files
        for (init_name, init_loss) in self.sorted_inits:
            os.remove(f"{init_name}.meta")
            os.remove(f"{init_name}.index")
            os.remove(f"{init_name}.data-00000-of-00001")

    def train(self, init_name):
        opts = self.opts

        restore_saver = tf.train.import_meta_graph(f"{init_name}.meta")
        restore_saver.restore(self.sess, f"./{init_name}")

        loss_v = None

        self.sess.run(self.reset_step)

        for i in range(opts['n_iterations']):

            loss_v, learning_rate_v = self.sess.run([self.loss, self.learning_rate])

            if self.verbosity > 0 or (i % self.opts['loss_freq'] == 0 and self.opts['loss_freq'] > 0):
                print("[%6d] %16.12f || %10.6f" % (i, loss_v, learning_rate_v))
            if self.verbosity > 1 or (i % self.opts['losses_freq'] == 0 and self.opts['losses_freq'] > 0):
                self.print_losses()
            if i % self.opts['plot_freq'] == 0 and self.opts['plot_freq'] > 0:
                self.get_model().plot()

            if loss_v < opts['eps']:
                if opts['verbosity'] >= 0:
                    self.print_losses()
                return loss_v
            else:
                self.sess.run(self.apply_grads)

        return loss_v


    #####################
    ## Core
    ####################

    def get_model(self):
        named_pt_assn, named_line_assn, named_circ_assn, segments, \
            unnamed_points, unnamed_lines, unnamed_circles_assn, ndgs, goals = self.run([
                self.name2pt, self.name2line, self.name2circ,
                self.segments, self.unnamed_points, self.unnamed_lines, self.unnamed_circles,
                self.ndgs, self.goals
            ])

        return Diagram(
            named_points=named_pt_assn, named_lines=named_line_assn, named_circles=named_circ_assn,
            segments=segments, seg_colors=self.seg_colors, unnamed_points=unnamed_points, unnamed_lines=unnamed_lines,
            unnamed_circles=unnamed_circles_assn, ndgs=ndgs, goals=goals)

    def run(self, x):
        return self.sess.run(x)

    def satisfies_goals(self):
        if not self.opts['enforce_goals']:
            return True

        goals = self.run(self.goals)
        for k, x in goals.items():
            if x > self.opts['eps'] * 10:
                return False
        return True

    def valid_model(self):
        if self.verbosity > 0:
            self.print_losses()
        if self.points_far_enough_away() and self.satisfies_goals():
            return True
        return False

    def solve(self):
        if self.has_loss:
            self.freeze()

        models = list()

        for i in range(self.n_tries):

            # Stop when we have enough
            if len(models) >= self.opts['n_models']:
                if self.has_loss: self.remove_inits()
                return models

            if not self.has_loss:
                self.run(tf.compat.v1.global_variables_initializer())
                if self.valid_model():
                    models.append(self.get_model())
            else:
                loss = None
                try:
                    loss = self.train(init_name=self.sorted_inits[i][0])
                except Exception as e:
                    if self.verbosity > 0:
                        print(f"ERROR: {e}")

                if loss is not None and loss < self.opts['eps']:
                    if self.valid_model():
                        models.append(self.get_model())
        if self.has_loss: self.remove_inits()
        return models
