#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  breakout_groups.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>

import os
from pathlib import Path
from inc import config as cfg
 


class BreakoutGroups():
    """ test the preformance of numpy array calcs""" 
    def func(self,):
        pass
 
 
if __name__ == '__main__':
    # set the config file working directory
    wkdir = str(Path(__file__).resolve().parent) + os.sep
    cfg.wkdir = wkdir
    cfg.incdir = wkdir + 'inc' + os.sep
    bg = BreakoutGroups()
    print(cfg,wkdir)