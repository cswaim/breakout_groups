#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  reports.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>

from pathlib import Path
from src import config as cfg
import logging
log = logging.getLogger(__name__)

from src.reports_interactions_matrix import InteractionsMatrix
from src.reports_cards import CardsReports

class Reports():
    """ Select and produce reports based on settings  """ 

    def __init__(self, autorun=False):
        """set up variables, import algorithm and run"""
        log.info(f"beg reporting")
        self.rim = True  # interactions matrix
        self.rcd = True  # card report
        # run the reports
        if autorun:
            self.run()
        log.info(f"end reporting")
 
    def run(self,):
        """run the algorithm"""
        # run selected reports
        if self.rim:
            rim = InteractionsMatrix(autorun=True)

        if self.rcd:
            rcd = CardsReports()
            rcd.run()
