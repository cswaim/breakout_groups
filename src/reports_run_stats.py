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

class RunStats():
    """ produce the interactions matrix and historgram reports
        and write pdf to data folder """

    def __init__(self, all_card_interactions=None):
        """init interactions stats"""
        if all_card_interactions is None:
            all_card_interactions=cfg.all_card_interactions
        self.all_interactions = self.build_interactions(all_card_interactions)
        # init stat variables
        self.inter_cnt = 0
        self.miss_inter_cnt = 0
        self.dup_inter_cnt = 0
        self.inter_ratio_tot = 0
        self.unique_inter_cnt = 0
        self.inter_ratio_unique = 0
        self.miss_inter_cnt = 0

        # possible unique interactions possible n(n-1)/2
        self.pui = math.comb(cfg.n_attendees, 2)
        self.maxpui = int(((cfg.group_size -1) * cfg.n_sessions * cfg.n_attendees) / 2)
        self.maxidivi = (cfg.group_size -1) * cfg.n_sessions
        # possible combinations n! / r!(n-r)!    r is group size
        self.puc = math.comb(cfg.n_attendees, cfg.group_size)
        self.gc = cfg.n_sessions * cfg.n_groups

    def gen_run_stats(self,):

        df = pd.DataFrame.from_dict(self.all_interactions)
        # from counter
        # df = pd.DataFrame.from_records(list(dict(cfg.all_card_interactions).items()), columns=['attendee','count'])
        # print(df)

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



        self.inter_ratio_tot = self.inter_cnt / self.pui
        self.unique_inter_cnt = self.inter_cnt - self.dup_inter_cnt
        self.inter_ratio_unique = self.unique_inter_cnt / self.pui
        # missed cnt is overstated
        self.miss_inter_cnt = self.pui - self.inter_cnt


        return df

    def gen_run_stats_orig(self,):

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

        self.inter_ratio_tot = self.inter_cnt / self.pui
        self.unique_inter_cnt = self.inter_cnt - self.dup_inter_cnt
        self.inter_ratio_unique = self.unique_inter_cnt / self.pui
        # missed cnt is overstated
        self.miss_inter_cnt = self.pui - self.inter_cnt


    def build_interactions(self, all_card_interactions=None):
        """create interactions dic with list of all interactions
           this converts the dict of counters to a dict of lists
        """
        if all_card_interactions is None:
            all_card_interactions=cfg.all_card_interactions

        interactions = {}
        for k, v in all_card_interactions.items():
            ia = []
            for i in range(cfg.n_attendees):
                ia.append(v[i])
            interactions[k] = ia
        return interactions
