import argparse
import sexpdata
import collections
import tensorflow.compat.v1 as tf
import scipy
import os
import matplotlib.pyplot as plt
import pdb
from tqdm import tqdm

from problem import Problem
from tf_optimizer import TfOptimizer
from sp_optimizer import ScipyOptimizer

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)
tf.disable_v2_behavior()
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description='Arguments for building a model that satisfies a set of geometry constraints')

    # General arguments
    parser.add_argument('--problem', '-p', action='store', type=str, help='Name of the file defining the set of constraints')
    parser.add_argument('--solver', action='store', type=str, help='Name of the constraint solving method -- options are scipy or tensorflow', default="tensorflow")
    parser.add_argument('--n_tries', action='store', dest='n_tries', type=int, default=1)
    parser.add_argument('--regularize_points', action='store', dest='regularize_points', type=float, default=1e-6)
    parser.add_argument('--make_distinct', action='store', dest='make_distinct', type=float, default=1e-2)
    parser.add_argument('--distinct_prob', action='store', dest='distinct_prob', type=float, default=0.2)
    parser.add_argument('--min_dist', action='store', dest='min_dist', type=float, default=0.1)
    parser.add_argument('--ndg_loss', action='store', dest='ndg_loss', type=float, default=1e-3)

    # Tensorflow arguments
    parser.add_argument('--learning_rate', action='store', dest='learning_rate', type=float, default=1e-1)
    parser.add_argument('--decay_steps', action='store', dest='decay_steps', type=float, default=1e3)
    parser.add_argument('--decay_rate', action='store', dest='decay_rate', type=float, default=0.7)
    parser.add_argument('--n_iterations', action='store', dest='n_iterations', type=int, default=5000)
    parser.add_argument('--eps', action='store', dest='eps', type=float, default=1e-3)

    args = parser.parse_args()

    # Read and preprocess the problem
    problem = Problem(args.problem)
    problem.preprocess()
    print(problem)

    # Compile to instructions
    problem.gen_instructions()
    instructions_str = "\nINSTRUCTIONS:\n{header}\n{i_strs}".format(
        header="-" * 13,
        i_strs = '\n'.join([str(i) for i in problem.instructions])
    )
    print(instructions_str)

    # Solve the constraint problem with the chosen solving method
    if args.solver == "tensorflow":

        g = tf.Graph()
        with g.as_default():

            solver = TfOptimizer(problem.instructions, args, g)
            solver.preprocess()
            filtered_models = solver.solve()
            # print(filtered_models)

    elif args.solver == "scipy":
        solver = ScipyOptimizer(problem.instructions, args)
        solver.preprocess()
        filtered_models = solver.solve()
        # print(filtered_models)

    else:
        raise NotImplementedError(f"Solver not implemented: {args.solver}")

    print(f"\n\nFound {len(filtered_models)} models")
    for m in filtered_models:
        m.plot()
