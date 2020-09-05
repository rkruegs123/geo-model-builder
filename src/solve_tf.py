import tensorflow.compat.v1 as tf
import tensorflow_probability as tfp
import itertools
import pdb

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

    def run(self, x):
        return self.sess.run(x)

    def solve(self):
        if self.has_loss:
            raise NotImplementedError("TODO: Implement training for SolveTF")

        assignments = list()
        for _ in range(self.opts.n_tries):
            if not self.has_loss:
                self.run(tf.compat.v1.global_variables_initializer())
                assignment = self.run(self.params)
                assignments.append(assignment)
            else:
                raise NotImplementedError("TODO: Implement training for SolveTF")
        return assignments
