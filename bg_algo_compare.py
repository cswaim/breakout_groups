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

from src import config as cfg
from breakout_groups import BreakoutGroups
from src import sessions_util as su
from src.plot_algo_compare import PlotAlgoCompare

loop_cnt = 20

def set_config():
    """set variables for system run"""
    cfg.report_cards = False
    cfg.report_interactions_matrix = False
    return

def run_event():
    """ run for a single event"""
    for x in range(loop_cnt):
        bg = BreakoutGroups()
        bg.run()

def set_algorithm(algo=su.get_algorithms()):
    """ this is a generator and will set the cfg algorithm options with each next call"""
    for a in algo:
        cfg.sys_group_algorithm = a[0]
        cfg.sys_group_algorithm_class = a[1]
        yield a

def main(args):
    """ create breakout goups for an event"""
    # get the cfg parameters
    cfg.cp.run()
    set_config()

    # setup generator
    algo_gen = set_algorithm()

    # use loop to get each generator output
    while True:
        try:
            next(algo_gen)
        except StopIteration:
            break
        print(cfg.sys_group_algorithm_class)
        for x in range(loop_cnt):
            bg = BreakoutGroups()
            bg.run()

    # plot results of csv file
    pac = PlotAlgoCompare(autorun=True)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
