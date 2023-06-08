#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  reports_interactions_matrix.py
#
#  Copyright 2023 cswaim <cswaim@jcrl.net>
"""
TODO:
1) add event_title, event_subtitle to config file
2) add event_beg_date & event_end_date to config file
"""


from pathlib import Path
import os
from datetime import datetime
from src import config as cfg

class CardsReports():
    """ produce the cards and write to data folder """
    header_template = """
    Date: {} {:^40}
    Time: {} {:^40}
    """

    def __init__(self, autorun=False):
        """init print the cards report"""
        self.hd1 = "test event"  # to be cfg.event_title
        self.hd2 = ""            # to be cfg.event_subtitle
        if autorun:
            self.run()

    def prt_header(self,):
        """print the card header"""
        dt = datetime.now()
        print(self.header_template.format(dt.strftime("%y-%m-%d"), self.hd1, dt.strftime("%H:%M:%S"), self.hd2))

    def run(self,):
        self.prt_header()


if __name__ == '__main__':
    # set the config file working directory
    wkdir = str(Path(__file__).resolve().parent) + os.pathsep
    cr = CardsReports()
    cr.run()