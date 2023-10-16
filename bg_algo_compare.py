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
import logging

from src import config as cfg
from breakout_groups import BreakoutGroups
from src import sessions_util as su

loop_cnt = 20

def set_config():
    """set variables for system run"""
    cfg.num_attendees = 14
    cfg.n_groups = 3
    cfg.n_sessions = 5
    cfg.group_size = 4
    cfg.report_cards = False
    cfg.report_interactions_matrix = False
    return

def run_event():
    """ run for a single event"""
    for x in range(loop_cnt):
        bg = BreakoutGroups()
        bg.run()

def set_algorithm(algo=su.get_algorithms()):
    """ from the list of algorithms return the next avaliable algorithm"""
    for a in algo:
        cfg.sys_group_algorithm_class = a[1]
        cfg.sys_group_algorithm = a[0]
        yield a

if __name__ == '__main__':
    """ create breakout goups for an event"""
    # get the cfg parameters
    cfg.cp.run()
    set_config()

    algo_gen = set_algorithm()
    while True:
        try:
            next(algo_gen)
        except StopIteration:
            break
        print(cfg.sys_group_algorithm_class)
        for x in range(loop_cnt):
            bg = BreakoutGroups()
            bg.run()