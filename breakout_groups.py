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
from src import config as cfg
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
        self.group_size = cfg.group_size
        self.n_groups = cfg.n_groups
        self.n_sessions = cfg.n_sessions
        self.attendees_list = cfg.attendees_list
        self.event = None
        self.seed = cfg.random_seed
        logger_setup.run()
        log.info("beg breakout-groups")

    def print_variables(self,):
        """print config variables"""
        print("")
        print(f"         algorithm: {cfg.sys_group_algorithm}")
        print(f"   algoritim_class: {cfg.sys_group_algorithm_class}")
        print("")
        print(f"    attendees_list: {cfg.attendees_list}")
        print(f"         attendees: {cfg.n_attendees}")
        print(f"        group_size: {cfg.group_size}")
        print(f"groups_per_session: {cfg.n_groups}")
        print(f"          sessions: {cfg.n_sessions}")
        print("")
        print(f"       random seed: {cfg.random_seed}")
        print("")

        cfg.print_config_vars(heading="Print All Variables")

    def run(self,):
        """create breakout groups for event"""
        log.info("beg event processing")
        self.print_variables()
        self.event = Event(self.seed)
        self.event.run()
        self.event.show_sessions()
        log.info("end event processing")


def main(args):
    """ create breakout goups for an event"""
    # get the cfg parameters
    cfg.cp.run()

    # get runtime sys args
    get_args()


    bg = BreakoutGroups()
    bg.run()
    log.info("end of breakout-groups")

def get_args():
    """get the args and edit"""
    help_arg = ["--help", "-h"]
    init_arg = ["--init", "-init", "init"]
    init_text = f"The config file has been created in {cfg.datadir}{cfg.cfg_flnm} "
    help_text = f"""
 This module runs the breakout group application, creating interaction reports
 and cards in the data folder {cfg.datadir}

 On the first run, the default config file is created in the data directory.  If
 the init parameter is passed, then the run exits and the config file can be
 modified.  Otherwise the run continues with the defaults.

 To rebuild the config file from the default cfg settings, delete the existing
 cfg file.  A rebuild can also be forced by changing the sys_cfg_version to 0

 The config file can be modified and the job rerun as needed.

 ex:
    python breakout_groups.py          (runs the app - the default)
    python breakout_groups init        (run one time for setup)
    python breakout_groups --help      (or -h  displays this text)

 If an arg of --help or -h is passed with the command, this message is
     printed
"""

    # if no args, run with default
    if len(sys.argv) > 1:
        # check for help
        if sys.argv[1] in help_arg:
            print(help_text)
            exit()
        # check for init
        if sys.argv[1] in init_arg:
            print(init_text)
            exit()

if __name__ == '__main__':
    """get and check the args and run compare """
    sys.exit(main(sys.argv))