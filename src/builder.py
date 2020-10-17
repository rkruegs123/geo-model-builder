import tensorflow.compat.v1 as tf
import os
import pdb
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
from tqdm import tqdm
import time

from tf_optimizer import TfOptimizer
from parse import parse_sexprs
from instruction_reader import InstructionReader


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)
tf.disable_v2_behavior()
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)



def build_aux(opts, show_plot=True, save_plot=False, outf_prefix=None, encode_fig=False):
    lines = opts['lines']

    cmds = parse_sexprs(lines)
    reader = InstructionReader(lines)
    instructions = reader.instructions

    verbosity = opts['verbosity']

    if verbosity >= 0:
        print("INPUT INSTRUCTIONS:\n{instrs_str}".format(instrs_str="\n".join([str(i) for i in instructions])))


    g = tf.Graph()
    with g.as_default():

        solver = TfOptimizer(instructions, opts,
                             reader.unnamed_points, reader.unnamed_lines, reader.unnamed_circles,
                             reader.segments, reader.seg_colors, g)
        solver.preprocess()
        filtered_models = solver.solve()
        # print(filtered_models)


    if verbosity >= 0:
        print(f"\n\nFound {len(filtered_models)} models")

    figs = list()
    for i, m in enumerate(filtered_models):
        # FIXME: Inconsistent return type
        if not (encode_fig or show_plot or save_plot):
            figs.append(m)
        else:
            figs.append(m.plot(show=show_plot, save=save_plot, fname=f"{outf_prefix}_{i}.png", return_fig=encode_fig))
    return figs


def build(opts, show_plot=True, save_plot=False, outf_prefix=None, encode_fig=False):
    if opts['n_models'] > 10:
        raise RuntimeError("Max # of models is 10")

    problem_given = ('lines' in opts or bool(opts['problem']))
    dir_given = 'dir' in opts and bool(opts['dir'])

    if problem_given and dir_given:
        raise RuntimeError("Please only supply one of --problem and --dir")

    if not (problem_given or dir_given):
        raise RuntimeError("Please provide either --problem or --dir")

    if problem_given:
        if 'lines' not in opts:
            opts['lines'] = open(opts['problem'], 'r').readlines()
        return build_aux(opts, show_plot=show_plot, save_plot=save_plot, outf_prefix=outf_prefix, encode_fig=encode_fig)
    else:
        dir_files = [f for f in listdir(opts['dir']) if isfile(join(opts['dir'], f)) and f[-1] != "~"]

        if opts['experiment']:

            from statistics import mean, stdev
            import itertools

            solve_map = { f: list() for f in dir_files }

            all_trial_data = list()

            all_trial_times = list()
            all_trial_success_times = list()
            all_trial_fail_times = list()

            n_trials = 1
            opts['verbosity'] = -1
            opts['plot_freq'] = -1
            opts['loss_freq'] = -1
            opts['losses_freq'] = -1

            for _ in tqdm(range(n_trials), desc="Trials"):
                trial_data = list()
                trial_times = list()
                trial_success_times = list()
                trial_fail_times = list()
                for f in tqdm(dir_files, desc="Problems"):
                    plt.close('all')

                    opts['lines'] = open(join(opts['dir'], f), 'r').readlines()
                    start = time.time()
                    models = build_aux(opts, show_plot=False, save_plot=False, outf_prefix=outf_prefix, encode_fig=False)
                    end = time.time()
                    time_elapsed = end - start
                    n_models = len(models)
                    solve_map[f].append(n_models)
                    trial_data.append(n_models)
                    trial_times.append(time_elapsed)

                    if n_models == opts['n_models']:
                        trial_success_times.append(time_elapsed)
                    elif n_models == 0:
                        trial_fail_times.append(time_elapsed)

                all_trial_data.append(trial_data)
                all_trial_times.append(trial_times)
                all_trial_success_times.append(trial_success_times)
                all_trial_fail_times.append(trial_fail_times)

            print(f"\n\nAll Trial Data:\n{all_trial_data}")
            print(f"\n\nSolve Map:\n{solve_map}")
            print("\n\n")

            all_n_models_per_file = [mean(t_data) for t_data in all_trial_data] # should have length 2
            avg_models_per_file = mean(all_n_models_per_file)
            std_models_per_file = stdev(all_n_models_per_file)


            # % Problems with at least one model
            all_n_models_with_gt0_models = [len([n for n in t_data if n > 0]) / len(dir_files) * 100 for t_data in all_trial_data]
            avg_perc_success = mean(all_n_models_with_gt0_models)
            std_perc_success = stdev(all_n_models_with_gt0_models)

            # (avg time per problem) per trial
            all_avg_times = [mean(time_data) for time_data in all_trial_times]
            avg_time = mean(all_avg_times)
            std_time = stdev(all_avg_times)

            all_avg_success_times = [mean(success_time_data) for success_time_data in all_trial_success_times]
            avg_success_time = mean(all_avg_success_times)
            std_success_time = stdev(all_avg_success_times)

            all_avg_fail_times = [mean(fail_time_data) for fail_time_data in all_trial_fail_times]
            avg_fail_time = mean(all_avg_fail_times)
            std_fail_time = stdev(all_avg_fail_times)

            print(f"Models per File: Avg {avg_models_per_file}, Sd {std_models_per_file}")
            print(f"% Problems with atleast 1 Model: Avg {avg_perc_success}, Sd {std_perc_success}")
            print(f"Avg Time per Problem (all): Avg {avg_time}, Sd {std_time}")
            print(f"Avg Time per Problem (success): Avg {avg_success_time}, Sd {std_success_time}")
            print(f"Avg Time per Problem (fail): Avg {avg_fail_time}, Sd {std_fail_time}")

        else:

            solve_map = dict()

            for f in dir_files:
                plt.close('all')

                opts['lines'] = open(join(opts['dir'], f), 'r').readlines()
                models = build_aux(opts, show_plot=False, save_plot=save_plot, outf_prefix=outf_prefix, encode_fig=True)
                solve_map[f] = len(models)

            for f, n_models in solve_map.items():
                print(f"{f}: {n_models}")
