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
        self.attendees = cfg.config.getint('DEFAULT','attendees')
        self.group_size = cfg.config.getint('DEFAULT','group_size')
        self.groups_per_session = cfg.config.getint('DEFAULT','groups_per_session')
        self.sessions = cfg.config.getint('DEFAULT','sessions')

        self.gen_attendees_list()

    def gen_attendees_list(self,):
        self.attendees_list = [x for x in range(self.members)]



 
if __name__ == '__main__':
    
    bg = BreakoutGroups()
