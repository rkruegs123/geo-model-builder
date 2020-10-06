import argparse
import pdb

from builder import build
from util import DEFAULTS


if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description='Arguments for building a model that satisfies a set of geometry constraints')

    # General arguments
    parser.add_argument('--problem', '-p', action='store', type=str, help='Name of the file defining the set of constraints')
    parser.add_argument('--solver', action='store', type=str, help='Name of the constraint solving method -- options are scipy or tensorflow', default=DEFAULTS["solver"])
    parser.add_argument('--n_tries', action='store', dest='n_tries', type=int, default=1)
    parser.add_argument('--regularize_points', action='store', dest='regularize_points', type=float, default=DEFAULTS["regularize_points"])
    parser.add_argument('--make_distinct', action='store', dest='make_distinct', type=float, default=DEFAULTS["make_distinct"])
    parser.add_argument('--distinct_prob', action='store', dest='distinct_prob', type=float, default=DEFAULTS["distinct_prob"])
    parser.add_argument('--min_dist', action='store', dest='min_dist', type=float, default=DEFAULTS["min_dist"])
    parser.add_argument('--ndg_loss', action='store', dest='ndg_loss', type=float, default=DEFAULTS["ndg_loss"])

    # Tensorflow arguments
    parser.add_argument('--learning_rate', action='store', dest='learning_rate', type=float, default=DEFAULTS["learning_rate"])
    parser.add_argument('--decay_steps', action='store', dest='decay_steps', type=float, default=DEFAULTS["decay_steps"])
    parser.add_argument('--decay_rate', action='store', dest='decay_rate', type=float, default=DEFAULTS["decay_rate"])
    parser.add_argument('--n_iterations', action='store', dest='n_iterations', type=int, default=DEFAULTS["n_iterations"])
    parser.add_argument('--eps', action='store', dest='eps', type=float, default=DEFAULTS["eps"])

    args = parser.parse_args()
    args = vars(args)

    lines = open(args['problem'], 'r').readlines()
    args['lines'] = lines

    build(args)
