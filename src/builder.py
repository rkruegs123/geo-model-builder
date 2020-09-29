import tensorflow.compat.v1 as tf
import os
import pdb

from point_compiler import PointCompiler
from tf_optimizer import TfOptimizer
from sp_optimizer import ScipyOptimizer
from parse import parse_sexprs
from instruction_reader import InstructionReader


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)
tf.disable_v2_behavior()
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

def build(opts, show_plot=True, save_plot=False, outf_prefix=None):
    grammar = opts['grammar']
    lines = opts['lines']
    solver = opts['solver']

    if grammar == "pointwise":
        # Read the problem
        compiler = PointCompiler(lines)

        # Compile to instructions
        compiler.compile()
        instructions = compiler.instructions
    elif grammar == "instructions":
        cmds = parse_sexprs(lines)
        reader = InstructionReader(lines)
        instructions = reader.instructions
        for instr in instructions:
            print(instr)
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
        raise NotImplementedError("Scipy solver is deprecated")
        '''
        solver = ScipyOptimizer(instructions, opts)
        solver.preprocess()
        filtered_models = solver.solve()
        '''
        # print(filtered_models)

    else:
        raise NotImplementedError(f"Solver not implemented: {solver}")

    print(f"\n\nFound {len(filtered_models)} models")
    for i, m in enumerate(filtered_models):
        m.plot(show=show_plot, save=save_plot, fname=f"{outf_prefix}_{i}.png")
