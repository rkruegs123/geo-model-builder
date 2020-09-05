import argparse
import sexpdata
import collections
import tensorflow.compat.v1 as tf
import scipy
import os

from problem import Problem
from constraint_system import ConstraintSystem
from solve_tf import SolveTF

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)
tf.disable_v2_behavior()
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description='Arguments for building a model that satisfies a set of geometry constraints')
    parser.add_argument('--problem', '-p', action='store', type=str, help='Name of the file defining the set of constraints')
    parser.add_argument('--solver', action='store', type=str, help='Name of the constraint solving method -- options are scipy or tensorflow', default="tensorflow")
    parser.add_argument('--n_tries', action='store', dest='n_tries', type=int, default=1)
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

    # Convert the instructions to a general constraint solving problem
    c_sys = ConstraintSystem(problem.instructions)

    # Solve the constraint problem with the chosen solving method
    if args.solver == "tensorflow":
        g = tf.Graph()
        with g.as_default():
            solver = SolveTF(c_sys, g, args)
            print(solver.params)
            unfiltered_models = solver.solve()
            print(unfiltered_models)
    else:
        raise NotImplementedError("Solver not implemented")
