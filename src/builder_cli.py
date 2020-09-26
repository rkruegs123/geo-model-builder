import argparse
import pdb

from builder import build


if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description='Arguments for building a model that satisfies a set of geometry constraints')

    # General arguments
    parser.add_argument('--problem', '-p', action='store', type=str, help='Name of the file defining the set of constraints')
    parser.add_argument('--solver', action='store', type=str, help='Name of the constraint solving method -- options are scipy or tensorflow', default="tensorflow")
    parser.add_argument('--grammar', action='store', type=str, help='Type of problem to be read in -- options are pointwise or multisorted', default="pointwise")
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

    build(vars(args))
