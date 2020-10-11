import tensorflow.compat.v1 as tf
import os
import pdb
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt

from point_compiler import PointCompiler
from tf_optimizer import TfOptimizer
from sp_optimizer import ScipyOptimizer
from parse import parse_sexprs
from instruction_reader import InstructionReader


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)
tf.disable_v2_behavior()
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)



def build_aux(opts, show_plot=True, save_plot=False, outf_prefix=None, encode_fig=False):
    lines = opts['lines']
    solver = opts['solver']

    cmds = parse_sexprs(lines)
    reader = InstructionReader(lines)
    instructions = reader.instructions

    if reader.problem_type == "compile":
        compiler = PointCompiler(instructions, reader.points)
        compiler.compile()
        final_instructions = compiler.instructions
    elif reader.problem_type == "instructions":
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
    figs = list()
    for i, m in enumerate(filtered_models):
        # m.plot(show=show_plot, save=save_plot, fname=f"{outf_prefix}_{i}.png")
        figs.append(m.plot(show=show_plot, save=save_plot, fname=f"{outf_prefix}_{i}.png", return_fig=encode_fig))
    return figs


def build(opts, show_plot=True, save_plot=False, outf_prefix=None, encode_fig=False):
    if opts['n_models'] > 10:
        raise RuntimeError("Max n_models is 10")

    problem_given = ('lines' in opts or opts['problem'])
    dir_given = 'dir' in opts

    if problem_given and dir_given:
        raise RuntimeError("Please only supply one of --problem and --dir")

    if not (problem_given or dir_given):
        raise RuntimeError("Please provide either --problem or --dir")

    if problem_given:
        if 'lines' not in opts:
            opts['lines'] = open(opts['problem'], 'r').readlines()
        return build_aux(opts, show_plot=show_plot, save_plot=save_plot, outf_prefix=outf_prefix, encode_fig=encode_fig)
    else:
        dir_files = [f for f in listdir(opts['dir']) if isfile(join(opts['dir'], f))]

        solve_map = dict()

        for f in dir_files:
            plt.close('all')

            opts['lines'] = open(join(opts['dir'], f), 'r').readlines()
            models = build_aux(opts, show_plot=False, save_plot=save_plot, outf_prefix=outf_prefix, encode_fig=True)
            solve_map[f] = len(models)

        for f, n_models in solve_map.items():
            print(f"{f}: {n_models}")
