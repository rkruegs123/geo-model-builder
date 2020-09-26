import tensorflow.compat.v1 as tf
import os

from point_compiler import PointCompiler
from tf_optimizer import TfOptimizer
from sp_optimizer import ScipyOptimizer
from parse import parse_sexprs


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)
tf.disable_v2_behavior()
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

def build(opts):
    grammar = opts['grammar']
    lines = opts['lines']
    solver = opts['solver']

    if grammar == "pointwise":
        # Read the problem
        compiler = PointCompiler(lines)

        # Compile to instructions
        compiler.compile()
        instructions = compiler.instructions
    elif grammar == "multisorted":
        cmds = parse_sexprs(lines)
        print(cmds)
        raise NotImplementedError("Still working on multisorted...")
    else:
        raise RuntimeError(f"Invalid grammar: {grammar}")

    # Solve the constraint problem with the chosen solving method
    if solver == "tensorflow":

        g = tf.Graph()
        with g.as_default():

            solver = TfOptimizer(instructions, opts, g)
            solver.preprocess()
            filtered_models = solver.solve()
            # print(filtered_models)

    elif solver == "scipy":
        solver = ScipyOptimizer(instructions, opts)
        solver.preprocess()
        filtered_models = solver.solve()
        # print(filtered_models)

    else:
        raise NotImplementedError(f"Solver not implemented: {solver}")

    print(f"\n\nFound {len(filtered_models)} models")
    for m in filtered_models:
        m.plot()
