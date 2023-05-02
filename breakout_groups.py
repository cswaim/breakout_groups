#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  breakout_groups.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>

# import os
# from pathlib import Path
# import math
# from itertools import combinations, chain
# import itertools as it

from src import config as cfg
from src.event import Event
from src.logger_setup import log

class BreakoutGroups():
    """ generate breakout groups """ 

    attendees_list = []

    n_attendees = 0
    group_size = 0
    n_groups = 0
    n_sessions = 0

    def __init__(self) -> None:
        """setup"""
        self.n_attendees = cfg.n_attendees
        self.group_size = cfg.group_size
        self.n_groups = cfg.n_groups
        self.n_sessions = cfg.n_sessions
        self.attendees_list = cfg.attendees_list

    def print_variables(self,):
        """print config variables"""
        print(f"    attendees_list: {cfg.attendees_list}")
        print(f"         attendees: {cfg.n_attendees}")
        print(f"        group_size: {cfg.group_size}")
        print(f"groups_per_session: {cfg.n_groups}")
        print(f"          sessions: {cfg.n_sessions}")
        print("")

    def run(self,):
        """create breakout groups for event"""
        self.print_variables()
        log.info("starting event processing")
        event = Event()
        event.run()
        for i, val in event.sess.sessions.items():
            print(f"Session {i:02} - {val}")


 
if __name__ == '__main__':
    log.info("start breakout-groups")
    bg = BreakoutGroups()
    bg.run()
    log.info("end of breakout-groups")
    
    
