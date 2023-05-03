#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sessions.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>

import importlib
import logging
#log = logging.getLogger('debug_logger')
log = logging.getLogger(__name__)

class Sessions():
    """ this is the driver for the the session generations""" 

    def __init__(self, algorithm, seed=None):
        # import module
        log.info(f"beg algorithm: {algorithm}")
        self.algorithm = algorithm
        #self.clsnm = clsnm
        self.sessions = []
        self.seed = seed
        self.load_algorithm()
        log.info(f"end of algorithm run")
 
    def load_algorithm(self, ):
        """ load the algorithm module and execute"""
        '''
            def __init__(self, module_name, class_name):
                """Constructor"""
                module = __import__(module_name)
                my_class = getattr(module, class_name)
                instance = my_class()
                print instance

                 self.amod = __import__(self.algorithm)
                acls = getattr(self.amod, self.clsnm)
                self.ci = acls()
                self.sessions = self.ci.gen_groups()
        '''
        s = __import__("src.{0}".format(self.algorithm))
        mod = getattr(s, self.algorithm)
        # self.cls = getattr(mod, self.clsnm)
        # ci = self.cls()
        # self.sessions = ci.build_sessions()
        self.sessions = mod.run()

