from pathlib import Path
import os
import io
import pandas as pd
import numpy as np
import seaborn as sns
import math
from datetime import datetime
from src import config as cfg
from src import sessions_util as su
from src import reports_util as rptu

class InteractionsMatrix():
    """ produce the interactions matrix and historgram reports
        and write pdf to data folder """

    def __init__(self, interactions):
        """init interactions stats"""
        self.all_interactions = self.build_interactions()
        self.inter_cnt = 0
        self.miss_inter_cnt = 0
        self.dup_inter_cnt = 0
        if autorun:
            self.run()

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
        self.maxpui = int(((cfg.group_size -1) * cfg.n_sessions * cfg.n_attendees) / 2)
        self.maxidivi = (cfg.group_size -1) * cfg.n_sessions
        self.inter_ratio_tot = self.inter_cnt / self.pui
        self.unique_inter_cnt = self.inter_cnt - self.dup_inter_cnt
        self.inter_ratio_unique = self.unique_inter_cnt / self.pui
        # missed cnt is overstated
        self.miss_inter_cnt = self.pui - self.inter_cnt

        # possible combinations n! / r!(n-r)!    r is group size
        self.puc = math.comb(cfg.n_attendees, cfg.group_size)
        self.gc = cfg.n_sessions * cfg.n_groups

        df=df.replace(0,"")

        return df
