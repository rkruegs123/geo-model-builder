import tensorflow.compat.v1 as tf
import tensorflow_probability as tfp
import itertools

class SolveTF:
    def __init__(self, c_sys, opts):
        self.constraint_system = c_sys
        tfcfg           = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
        self.sess       = tf.Session(graph=graph, config=tfcfg)
        self.has_loss = False
        self.opts       = opts

        # FIXME: Process the constraint system into a computation graph

    def run(self, x):
        return self.sess.run(x)

    def build_diagrams(self):
        if self.has_loss:
            raise NotImplementedError("TODO: Implement training for SolveTF")

        for _ in range(self.opts.n_tries):
            if not self.has_loss:
                self.run(tf.compat.v1.global_variables_initializer())
                try:
                    pass
                    # check_points_far_enough_away(self.run(self.name2pt), self.opts.min_dist)
                    # self.save_diagram()
                    # if opts.verbose: self.print_losses()
                    # if opts.plot: self.plot()
                except Exception as e:
                    raise NotImplementedError("TODO: Better error message...")
            else:
                raise NotImplementedError("TODO: Implement training for SolveTF")
