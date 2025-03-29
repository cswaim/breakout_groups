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
from src import bg_parser
from src import sessions_util as su
from src.plot_algo_compare import PlotAlgoCompare
from src import reports_util as rptu
from src.algo_compare_analysis import AlgoCompareAnalysis

#loop_cnt = 50

def set_config():
    """set variables for system run"""
    cfg.report_cards = False
    cfg.report_interactions_matrix = False
    cfg.sys_run_stats_csv = 'run_stats_compare.csv'
    cfg.sys_run_stats_txt = 'run_stats_compare.txt'
    # calc group size
    n_groups, cfg.group_size = su.set_n_groups(0)
    return

def set_algorithm(algo=None):
    """ this is a generator and will set the cfg algorithm options with each next call
        algo is a list of module, class pairs
        algo = [['m1','cm1'],['m2','cm2'],['m3','cm3']]
    """
    if algo is None:
        algo = su.get_algorithms()
    for a in algo:
        cfg.sys_group_algorithm = a[0]
        cfg.sys_group_algorithm_class = a[1]
        yield a

def main(args):
    """ create breakout goups for an event"""

    # get the command line parameters
    parser = bg_parser.get_parser()
    parms = parser.parse_args()
    bg_parser.set_cfg_values(parms, cfg)
    loop_cnt = parms.loop_cnt

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


if __name__ == '__main__':
    """get and check the args and run compare """
    sys.exit(main(sys.argv))
