#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bg_algo_compare.py
#
#  compare the effectiveness and performance of differnt algorithms
#  the various algoritms are defined in tests/conftest.py
#  this will run 10 loops of each algorithm, capture the results in
#  a csv and then plot the data.
#
#  Copyright 2023 cswaim <cswaim@tpginc.net>


import os
import sys
import logging
from contextlib import redirect_stdout
from pathlib import Path

from src import config as cfg
from breakout_groups import BreakoutGroups
from src import sessions_util as su
from src.plot_algo_compare import PlotAlgoCompare
from src import reports_util as rptu
from src.algo_compare_analysis import AlgoCompareAnalysis

loop_cnt = 50

def set_config():
    """set variables for system run"""
    cfg.report_cards = False
    cfg.report_interactions_matrix = False
    cfg.sys_run_stats_csv = 'run_stats_compare.csv'
    cfg.sys_run_stats_txt = 'run_stats_compare.txt'
    return

def set_algorithm(algo=su.get_algorithms()):
    """ this is a generator and will set the cfg algorithm options with each next call"""
    for a in algo:
        cfg.sys_group_algorithm = a[0]
        cfg.sys_group_algorithm_class = a[1]
        yield a

def main(args):
    """ create breakout goups for an event"""
    # get runtime sys args
    get_args()

    # get the cfg parameters
    cfg.cp.run()
    set_config()

    # print config
    rptu.print_header(hd1='Running with the following event config')
    rptu.print_event_parms_limited()
    print(f"  Running {loop_cnt} loops for each algorithm ")
    for a in su.get_algorithms():
        print(f"     module: {a[0]}, class: {a[1]}"  )
    print("")

    # setup generator
    algo_gen = set_algorithm()

    # set out file name
    cdir = os.getcwd()
    flname = cfg.sys_run_stats_txt.split(".txt")
    flname = flname[0] + "_all.txt"
    ofl = f'{cfg.datadir}{flname}'
    # delete the file
    with open(ofl, 'w') as f:
        f.write("")

    # del compare csv file
    Path(f'{cfg.datadir}{cfg.sys_run_stats_csv}').unlink(missing_ok=True)

    # use loop to get each generator output
    while True:
        try:
            next(algo_gen)
        except StopIteration:
            break
        # print(cfg.sys_group_algorithm_class)

        # redirect to file
        with open(ofl, 'a') as f:
            with redirect_stdout(f):
                for x in range(loop_cnt):
                    cfg.random_seed = None
                    bg = BreakoutGroups()
                    bg.run()

    # plot results of csv file
    algo_cnt = len(su.get_algorithms())
    pac = PlotAlgoCompare(autorun=True,)
    aca = AlgoCompareAnalysis(autorun=True)

def get_args():
    """get the args and edit"""
    global loop_cnt
    help_arg = ["--help", "-h"]

    # if no args, run with default
    if len(sys.argv) > 1:
        # check for help
        if sys.argv[1] in help_arg:
            print(help_text)
            exit()
        else:
            # set the loop_cnt
            try:
                loop_cnt = int(sys.argv[1])
            except:
                print(sys.argv, type(sys.argv[1]))
                print(get_arg_err_txt())
                exit()

def get_arg_err_txt():
    """build and return the arg error msg
        only run when arg > 1
    """

    arg_err_txt = f"""
 The arg must be --help, -h, or an integer
   received arg:  {sys.argv[1]}
"""
    return arg_err_txt

help_text = """
 This module compares the various algorithms by running each algorithm
 20 times, recording the metrics of the run in a csv and then ploting
 the results.

 ex:
    python bg_algo_compare.py          (runs 50 loops - the default)
    python bg_algo_compare.py 35       (run 35 loops)
    python bg_algo_compare.py --help    (or -h  displays this text)

 If an arg of --help or -h is passed with the command, this message is
     printed

 The only other accepted arg is an integer to set the loop-cnt. The default
 is 20.
"""


if __name__ == '__main__':
    """get and check the args and run compare """
    sys.exit(main(sys.argv))
