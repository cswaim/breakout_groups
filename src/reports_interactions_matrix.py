#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  reports_interactions_matrix.py
#
#  Copyright 2023 cswaim <cswaim@tpginc.net>

from pathlib import Path
import os
import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime
from src import config as cfg
from src import report_utils as rptu

class InteractionsMatrix():
    """ produce the interactions matrix and historgram reports
        and write pdf to data folder """

    def __init__(self, autorun=False):
        """init interactions matrix report"""
        self.all_interactions = self.build_interactions()
        if autorun:
            self.run()

    def build_interactions(self,):
        """create interactions dic with all counts"""

        interactions = {}
        for k, v in cfg.all_card_interactions.items():
            #ia = {}
            ia = []
            for i in range(cfg.n_attendees):
                # ia[i] = v[i]
                ia.append(v[i])
            interactions[k] = ia
        return interactions

    def gen_matrix(self,):

        df = pd.DataFrame.from_dict(self.all_interactions)

        # set the lower half of df to 0
        for i, row in df.iterrows():
            # set diagonal to zero
            df.iloc[i, i] = 0
            # set lower half to zero
            for c in range(0, i):
                df.iloc[i,c] = 0

        hd1 = "Interactions Matrix"
        hd2  = ""
        col_hd1 = "| Attendees  ->"
        col_hd2 = "v  "
        rptu.print_header(hd1, hd2, col_hd1, col_hd2)

        df=df.replace(0,"")

        print(df)

        # index = df.index
        # index.name = "id"

        cm=sns.color_palette("coolwarm", as_cmap=True)

        df=df.replace(0,np.NaN)
        df.style.background_gradient(cmap=cm,vmin=0,vmax=cfg.group_size).highlight_null('black')
        # print(df)


    def show_ascii_histogram(self,):
        """Simple horizontal histogram of attendee interactions"""
        # Count the number of interactions that have a value of
        # 0, 1, etc
        # Create a simple histogram to show the distribution
        from collections import Counter

        hd1 = "Interactions Histogram"
        hd2  = ""
        col_hd1 = "Inter     Num      Histogram"
        col_hd2 = "Count   Atendees  "
        rptu.print_header(hd1, hd2, col_hd1, col_hd2)

        r = Counter()
        for i, v in cfg.all_card_interactions.items():
            r = r + v
        rows = Counter(r.values())
        rptu.print_dtl("")
        for row in sorted(rows):
             line = f" {row:^5}    {rows[row]:^5}     {'*' * rows[row]} "
             rptu.print_dtl(line)
        pass

    def run(self,):
        self.gen_matrix()
        print("")
        self.show_ascii_histogram()
        print("")


if __name__ == '__main__':
    # set the config file working directory
    wkdir = str(Path(__file__).resolve().parent) + os.pathsep
    cl = InteractionsMatrix()