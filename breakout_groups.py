#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  breakout_groups.py
#
#  run the breakout groups system for event configured in
#  data/breakout_groups.cfg
#
#  Copyright 2023 cswaim <cswaim@tpginc.net>

import sys
import os
import random
from math import floor
from src import config as cfg
from src import bg_parser
from src.event import Event
from src import logger_setup
import logging
log = logging.getLogger(__name__)

class BreakoutGroups():
    """ generate breakout groups """

    attendees_list = []

    n_attendees = 0
    group_size = 0
    n_groups = 0
    n_sessions = 0

    def __init__(self, ) -> None:
        """setup"""
        self.n_attendees = cfg.n_attendees

        self.n_groups = cfg.n_groups
        self.n_sessions = cfg.n_sessions
        self.attendees_list = cfg.attendees_list
        self.event = None
        self.seed = self.gen_seed()

        # set group size
        if cfg.group_size > 0:
            self.group_size = cfg.group_size
        else:
            cfg.group_size = floor(cfg.n_attendees / cfg.n_groups)

        logger_setup.run()
        log.info("beg breakout-groups")

    def gen_seed(self):
        """set the cfg.random_seed"""
        if cfg.random_seed is None:
            seed = random.randrange(100000000)
            cfg.random_seed = seed
        else:
            seed = cfg.random_seed

        return seed

    def print_variables(self,):
        """print config variables"""
        print("")
        print(f"       config file: {cfg.cfg_flnm}")
        print(f"         algorithm: {cfg.sys_group_algorithm}")
        print(f"   algoritim_class: {cfg.sys_group_algorithm_class}")
        print("")
        print(f"    attendees_list: {cfg.attendees_list}")
        print(f"         attendees: {cfg.n_attendees}")
        print(f"        group_size: {cfg.group_size}")
        print(f"groups_per_session: {cfg.n_groups}")
        print(f"          sessions: {cfg.n_sessions}")
        print(f"num of extra cards: {cfg.n_extra_cards}")
        print("")
        print(f"       random seed: {cfg.random_seed}")
        print("")

        # cfg.print_config_vars(heading="Print All Variables")

    def run(self,):
        """create breakout groups for event"""
        log.info("beg event processing")
        self.print_variables()
        self.event = Event(self.seed)
        self.event.run()
        log.info("end event processing")


def main(args):
    """ create breakout goups for an event"""

    # get the cfg parameters
    cfg.cp.run()

    # get the command line parameters
    parser = bg_parser.get_parser()
    parms = parser.parse_args()
    bg_parser.set_cfg_values(parms, cfg)

    bg = BreakoutGroups()
    bg.run()
    log.info("end of breakout-groups")

if __name__ == '__main__':
    """get and check the args and run compare """
    sys.exit(main(sys.argv))