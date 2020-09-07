import tensorflow.compat.v1 as tf
import tensorflow_probability as tfp
import itertools
import pdb
import random

from comp_geo import Point, dist

'''

Next steps:

Need an example problem that has a loss/assert, or a parameterize at the very least...

Then, we can test with a training loop. Want to confirm that we can get models for those that require a training loop! Once we are this far (proving our representation for a constraint problem will do), can convert to a plot, and start filling things in...

'''

tfd = tfp.distributions

class SolveTF:
    def __init__(self, c_sys, graph, opts):
        self.constraint_system = c_sys
        tfcfg           = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
        self.sess       = tf.Session(graph=graph, config=tfcfg)
        self.has_loss = bool(c_sys.losses)
        self.opts       = opts

        self.params = dict()
        for p in c_sys.params:
            if p.initialization == "uniform":
                lo, hi = p.args
                init = tf.random_uniform_initializer(minval=lo, maxval=hi)
                self.params[p.name] = tf.compat.v1.get_variable(name=p.name, shape=[], dtype=tf.float64, initializer=init)
            else:
                raise NotImplementedError("Unsupported sampling method")

        # FIXME: Need to populate losses
        self.losses = dict()

        pdb.set_trace()

        self.name2pt = { n : Point(self.expr2tf(val.x), self.expr2tf(val.y)) for n, val in c_sys.name2pt.items() }


    def train(self):
        opts = self.opts
        self.sess.run(self.reset_step)
        self.sess.run(tf.compat.v1.global_variables_initializer())

        loss_v = None

        for i in range(opts.n_iterations):
            loss_v, learning_rate_v = self.sess.run([self.loss, self.learning_rate])
            '''
            if i > 0 and i % opts.print_freq == 0:
                if opts.verbose: print("[%6d] %16.12f || %10.6f" % (i, loss_v, learning_rate_v))
                if opts.verbose > 1: self.print_losses()
                if opts.plot > 1: self.plot()
            '''
            if loss_v < opts.eps:
                '''
                check_points_far_enough_away(self.run(self.name2pt), self.opts.min_dist)
                if opts.verbose: print("DONE: %f" % loss_v)
                if opts.verbose: self.print_losses()
                if opts.plot: self.plot()
                '''
                return loss_v
            else:
                self.sess.run(self.apply_grads)

        return loss_v



    def run(self, x):
        return self.sess.run(x)

    def solve(self):
        if self.has_loss:
            self.freeze()

        assignments = list()
        for _ in range(self.opts.n_tries):
            if not self.has_loss:
                self.run(tf.compat.v1.global_variables_initializer())
                assignment = self.run(self.params)
                assignments.append(assignment)
            else:
                # raise NotImplementedError("TODO: Implement training for SolveTF")
                loss = None
                try:
                    loss = self.train()
                except Exception as e:
                    print("ERROR: %s ..." % (str(e)))
                if loss is not None and loss < self.opts.eps:
                    print("got assignment via training!")
                    assignment = self.run(self.params)
                    assignments.append(assignment)
        return assignments

    def mk_non_zero(err):
        res = tf.reduce_mean(tf.exp(- (err ** 2) * 20))
        tf.check_numerics(res, message="mk_non_zero")
        return res

    def mk_zero(err):
        res = tf.reduce_mean(err**2)
        tf.check_numerics(res, message="mk_zero")
        return res

    def register_loss(self, key, val, weight=1.0):
        k = key + ("" if len(vals) == 1 else "_" + str(i+1))
        assert(not k in self.losses)
        # TF has a bug that causes nans when differentiating something exactly 0
        self.losses[k] = weight * mk_zero(val + 1e-6 * (random.random() / 2))

    def regularize_points(self):
        norms = tf.cast([self.point_norm(p) for p in self.name2pt.values()], dtype=tf.float64)
        self.losses["points"] = self.opts.regularize_points * tf.reduce_mean(norms)

    def make_points_distinct(self):
        if random.random() < self.opts.distinct_prob:
            distincts = tf.cast([dist(A, B) for A, B in itertools.combinations(self.name2pt.values(), 2)], tf.float64)
            dloss     = tf.reduce_mean(mk_non_zero(distincts))
            self.losses["distinct"] = self.opts.make_distinct * dloss

    def freeze(self):
        opts = self.opts
        self.regularize_points()
        self.make_points_distinct()
        self.loss = sum(self.losses.values())
        self.global_step = tf.train.get_or_create_global_step()
        self.learning_rate = tf.train.exponential_decay(
            global_step=self.global_step,
            learning_rate=opts.learning_rate,
            decay_steps=opts.decay_steps,
            decay_rate=opts.decay_rate,
            staircase=False)
        optimizer         = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
        gs, vs            = zip(*optimizer.compute_gradients(self.loss))
        self.apply_grads  = optimizer.apply_gradients(zip(gs, vs), name='apply_gradients', global_step=self.global_step)
        self.reset_step   = tf.assign(self.global_step, 0)


    #####################
    ## Expr Utilities
    ####################

    def point2tf(self, p):
        return tf.cast([p.x, p.y], dtype=tf.float64)

    def point_norm(self, p):
        return tf.norm(self.point2tf(p), ord=2)

    def expr2tf_aux(self, expr):
        op = expr.op
        if op == "const":
            [x] = expr.args
            # Note that we aren't using tf.constant here
            return x
        elif op == "var":
            [var_name] = expr.args
            if var_name not in self.params:
                raise RuntimeError(f"[expr2tf_aux] Var not found in self.params: {var_name}")
            return self.params[var_name]
        elif op == "cos":
            [x] = expr.args
            return tf.math.cos(self.expr2tf_aux(x))
        elif op == "sin":
            [x] = expr.args
            return tf.math.sin(self.expr2tf_aux(x))
        elif op == "acos":
            [x] = expr.args
            return tf.math.acos(self.expr2tf_aux(x))
        elif op == "tanh":
            [x] = expr.args
            return tf.nn.tanh(self.expr2tf_aux(x))
        elif op == "sum":
            xs = expr.args
            return tf.reduce_sum([self.expr2tf_aux(x) for x in xs])
        elif op == "sqrt":
            [x] = expr.args
            return tf.sqrt(self.expr2tf_aux(x))
        elif op == "sigmoid":
            [x] = expr.args
            return tf.nn.sigmoid(self.expr2tf_aux(x))
        elif op == "mul":
            [x1, x2] = expr.args
            return self.expr2tf_aux(x1) * self.expr2tf_aux(x2)
        elif op == "add":
            [x1, x2] = expr.args
            return self.expr2tf_aux(x1) + self.expr2tf_aux(x2)
        elif op == "sub":
            [x1, x2] = expr.args
            return self.expr2tf_aux(x1) - self.expr2tf_aux(x2)
        elif op == "div":
            [x1, x2] = expr.args
            return self.expr2tf_aux(x1) / self.expr2tf_aux(x2)
        elif op == "pow":
            [x1, x2] = expr.args
            return self.expr2tf_aux(x1) ** self.expr2tf_aux(x2)
        elif op == "neg":
            [x] = expr.args
            return -self.expr2tf_aux(x)
        else:
            raise NotImplementedError(f"[expr2tf_aux] Op not implemented: {op}")

    def expr2tf(self, expr):
        op = expr.op
        if op == "const":
            [x] = expr.args
            return tf.constant(x, dtype=tf.float64)
        else:
            return self.expr2tf_aux(expr)
