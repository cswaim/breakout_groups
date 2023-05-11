#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sessions.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>

import sys
import importlib
import logging
import traceback
from src import config as cfg
log = logging.getLogger(__name__)

class Sessions():
    """ this is the driver for the the session generations""" 

    def __init__(self, seed=None, autorun=True):
        """set up variables, import algorithm and run"""
        log.info(f"beg algorithm: {cfg.sys_group_algorithm}/{cfg.sys_group_algorithm_class}")
        self.algorithm = cfg.sys_group_algorithm
        self.algorithm_class = cfg.sys_group_algorithm_class
        self.sessions = {}
        self.interactions = {}
        self.seed = seed
        self.autorun = autorun
        self.load_algorithm()
        # run the algorithm
        if self.autorun:
            self.run_algorithm()
        log.info(f"end of algorithm run")
 
    def load_algorithm(self, ):
        """ load the algorithm module and execute"""
        # import the src modules 
        try:
            s = __import__("src.{0}".format(self.algorithm))
        except Exception as e:
            log.error(f"import of {self.algorithm} failed")
            log.error(traceback.format_exc())
            raise SystemExit()

        # get the module
        try:
            mod = getattr(s, self.algorithm)
        except Exception as e:
            log.error(f"the module {self.algoritm} was not found")
            log.error(traceback.format_exc())
            raise SystemExit()

        # get the class
        try:
           self.cls = getattr(mod, self.algorithm_class)
        except Exception as e:
            log.error(f"the class {self.algorithm_class} was not found in {self.algorithm}")
            log.error(traceback.format_exc())
            raise SystemExit()

        # instantiate the algorithm class 
        self.ac = self.cls()

    def run_algorithm(self,):
        """run the algorithm"""
        self.ac.run()
        # get the sessesions and interactions from algorithm
        self.sessions = self.ac.sessions
        if hasattr(self.ac,'interactions'):
            self.interactions = self.ac.interactions
