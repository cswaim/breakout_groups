#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  breakout_groups.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>

import os
from pathlib import Path
import math
from itertools import combinations, chain
import itertools as it

from src import config as cfg

class BreakoutGroups():
    """ generate breakout groups """ 

    attendees_list = []

    attendees = 0
    group_size = 0
    groups_per_session = 0
    sessions = 0

    def __init__(self) -> None:
        """setup"""
        self.attendees = cfg.n_attendees
        self.group_size = cfg.group_size
        self.groups_per_session = cfg.n_groups
        self.sessions = cfg.n_sessions
        self.attendees_list = cfg.attendees_list

    def print_variables(self,):
        """print the variables refereced two ways"""
        print("")
        print("variables can be refenced as self.xxx if set in init")
        print(f"    attendees_list: {self.attendees_list}")
        print(f"         attendees: {self.attendees}")
        print(f"        group_size: {self.group_size}")
        print(f"groups_per_session: {self.groups_per_session}")
        print(f"          sessions: {self.sessions}")
        print("or variables can be refenced directly from the cfg module as cfg.xxxx")
        print(f"    attendees_list: {cfg.attendees_list}")
        print(f"         attendees: {cfg.n_attendees}")
        print(f"        group_size: {cfg.group_size}")
        print(f"groups_per_session: {cfg.n_groups}")
        print(f"          sessions: {cfg.n_sessions}")



 
if __name__ == '__main__':
    
    bg = BreakoutGroups()
    bg.print_variables()
