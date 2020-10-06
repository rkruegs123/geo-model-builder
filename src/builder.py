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
    lines = opts['lines']
    solver = opts['solver']

    cmds = parse_sexprs(lines)
    reader = InstructionReader(lines)
    instructions = reader.instructions


    if reader.problem_type == "compile":
        compiler = PointCompiler(instructions, reader.points)
        compiler.compile()
        final_instructions = compiler.instructions
    elif reader.problem_tpye == "instructions":
        final_instructions = instructions
    else:
        raise RuntimeError("[build] Did not properly set problem type")


    # Solve the constraint problem with the chosen solving method
    if solver == "tensorflow":

        g = tf.Graph()
        with g.as_default():

            solver = TfOptimizer(final_instructions, opts, g)
            solver.preprocess()
            filtered_models = solver.solve()
            # print(filtered_models)

    elif solver == "scipy":
        raise NotImplementedError("Scipy solver is deprecated")
        '''
        solver = ScipyOptimizer(final_instructions, opts)
        solver.preprocess()
        filtered_models = solver.solve()
        '''
        # print(filtered_models)

    else:
        raise NotImplementedError(f"Solver not implemented: {solver}")

    print(f"\n\nFound {len(filtered_models)} models")
    for i, m in enumerate(filtered_models):
        m.plot(show=show_plot, save=save_plot, fname=f"{outf_prefix}_{i}.png")
