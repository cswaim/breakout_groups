#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  reports_interactions_matrix.py
#
#  Copyright 2023 cswaim <cswaim@tpginc.net>

from pathlib import Path
import os
import io
import pandas as pd
import numpy as np
import seaborn as sns
import math
from datetime import datetime
from src import config as cfg
from src import report_utils as rptu

class InteractionsMatrix():
    """ produce the interactions matrix and historgram reports
        and write pdf to data folder """

    def __init__(self, autorun=False):
        """init interactions matrix report"""
        self.all_interactions = self.build_interactions()
        self.inter_cnt = 0
        self.miss_inter_cnt = 0
        self.dup_inter_cnt = 0
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
                df.iloc[i, c] = 0

        # event run performance calculations

        # reset counters
        self.inter_cnt = 0
        self.miss_inter_cnt = 0
        self.dup_inter_cnt = 0

        for i, row in df.iterrows():
            for c in row:
                if c > 0:
                    self.inter_cnt += 1
                if c == 0:
                    self.miss_inter_cnt += 1
                if c > 1:
                    self.dup_inter_cnt += 1


        # possible unique interactions possible n(n-1)/2
        self.pui = math.comb(cfg.n_attendees, 2)

        # possible combinations n! / r!(n-r)!    r is group size
        self.puc = math.comb(cfg.n_attendees, cfg.group_size)
        self.gc = cfg.n_sessions * cfg.n_groups

        df=df.replace(0,"")

        return df

    def sytle_df_graphic(self, df):
        """
            The following code styles the display of the dataframe for graphic
            output

            not used, kept as doc
        """

        index = df.index
        index.name = "id"

        cm=sns.color_palette("coolwarm", as_cmap=True)

        df=df.replace(0,np.NaN)
        df.style.background_gradient(cmap=cm,vmin=0,vmax=cfg.group_size).highlight_null('black')


    def print_matrix(self, df, fileobj=None):
        """print the dataframe """
        hd1 = "Interactions Matrix"
        hd2  = ""
        col_hd1 = "| Attendees  ->"
        col_hd2 = "v  "
        rptu.print_header(hd1, hd2, col_hd1, col_hd2, fileobj=fileobj)

        print(df, file=fileobj)

        print("\n\n", file=fileobj)
        print("Run Analysis \n", file=fileobj)
        print(f"           Unique interactions: {self.inter_cnt}", file=fileobj)
        print(f"  Possible Unique interactions: {self.pui}", file=fileobj)
        print(f"                effective rate: {self.inter_cnt / self.pui:0.2}", file=fileobj)
        print(f"     Num orphaned interactions: {self.miss_inter_cnt}", file=fileobj)
        print(f"    Num duplicate interactions: {self.dup_inter_cnt}", file=fileobj)
        print("", file=fileobj)
        print(f"            group combinations: {self.gc}", file=fileobj)
        print(f"   Possible group combinations: {self.puc}", file=fileobj)



    def show_ascii_histogram(self, fileobj=None):
        """Simple horizontal histogram of attendee interactions"""
        # Count the number of interactions that have a value of
        # 0, 1, etc
        # Create a simple histogram to show the distribution
        from collections import Counter

        hd1 = "Interactions Histogram"
        hd2  = ""
        col_hd1 = "Inter     Num      Histogram"
        col_hd2 = "Count   Atendees  "
        rptu.print_header(hd1, hd2, col_hd1, col_hd2, fileobj=fileobj)

        r = Counter()
        for i, v in cfg.all_card_interactions.items():
            r = r + v
        rows = Counter(r.values())
        rptu.print_dtl("", fileobj=fileobj)
        for row in sorted(rows):
             line = f" {row:^5}    {rows[row]:^5}     {'*' * rows[row]} "
             rptu.print_dtl(line, fileobj=fileobj)
        pass

    def run(self,):
        with open(f'{cfg.datadir}interactions_reports.txt', 'w') as itxt:
            # make file obj available to all methods
            self.itxt = itxt
            df = self.gen_matrix()
            self.print_matrix(df)
            self.print_matrix(df, fileobj=itxt)
            itxt.write("\n\n\n\n")
            print("\n\n")
            self.show_ascii_histogram()
            self.show_ascii_histogram(fileobj=itxt)
            print("")


if __name__ == '__main__':
    # set the config file working directory
    wkdir = str(Path(__file__).resolve().parent) + os.pathsep
    cl = InteractionsMatrix()