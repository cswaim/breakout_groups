#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  reports_interactions_matrix.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>


 
from pathlib import Path
import os
from src import config as cfg

class CardsReports():
    """ produce the cards and write to data folder """ 
    def __init__(self, autorun=False):
        """init print the cards report"""
        if autorun:
            self.run()

    def run(self,):
        pass
 
 
if __name__ == '__main__':
    # set the config file working directory
    wkdir = str(Path(__file__).resolve().parent) + os.pathsep
    cr = CardsReports()
    cr.run()