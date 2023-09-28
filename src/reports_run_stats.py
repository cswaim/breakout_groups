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

    def __init__(self, all_card_interactions=None, autorun=False):
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
        if autorun:
            self.run()

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

    def print_stats(self, fileobj=None):
        """print the dataframe """
        hd1 = "Run Statistics"
        hd2  = None
        col_hd1 = None
        col_hd2 = None
        rptu.print_header(hd1, hd2, col_hd1, col_hd2, fileobj=fileobj)

        print("\n\n", file=fileobj)
        print(f"                         algorithm: {cfg.sys_group_algorithm}", file=fileobj)
        print(f"                   algoritim_class: {cfg.sys_group_algorithm_class}", file=fileobj)
        print("", file=fileobj)
        print(f"attendees_list: {cfg.attendees_list}", file=fileobj)
        print("", file=fileobj)
        print(f"                         attendees: {cfg.n_attendees}", file=fileobj)
        print(f"                        group_size: {cfg.group_size}", file=fileobj)
        print(f"                groups_per_session: {cfg.n_groups}", file=fileobj)
        print(f"                          sessions: {cfg.n_sessions}", file=fileobj)
        print("", file=fileobj)
        print(f"                Total Interactions: {self.inter_cnt}", file=fileobj)
        print(f"               Unique Interactions: {self.unique_inter_cnt}", file=fileobj)
        print(f"            Duplicate Interactions: {self.dup_inter_cnt}", file=fileobj)
        print(f"      Possible Unique interactions: {self.pui}", file=fileobj)
        print(f"         Max Possible interactions: {self.maxpui}", file=fileobj)
        print(f"       Max Individual interactions: {self.maxidivi}", file=fileobj)
        print(f"     Tot effective rate (tot/poss): {self.inter_ratio_tot:0.2}", file=fileobj)
        print(f" Unique effective rate (uniq/poss): {self.inter_ratio_unique:0.2}", file=fileobj)
        print(f"         Num orphaned interactions: {self.miss_inter_cnt}", file=fileobj)
        print(f"        Num duplicate interactions: {self.dup_inter_cnt}", file=fileobj)
        print("", file=fileobj)
        print(f"                group combinations: {self.gc}", file=fileobj)
        print(f"       Possible group combinations: {self.puc}", file=fileobj)

        """list the sessions"""
        print("\n\n", file=fileobj)
        for i, val in cfg.sessions.items():
            print(f"Session {i:02} - {val}", file=fileobj)

    def run(self,):
        with open(f'{cfg.datadir}run_stats.txt', 'w') as itxt:
            # make file obj available to all methods
            self.itxt = itxt
            # calc the stats
            self.gen_run_stats()
            self.print_stats()
            self.print_stats( fileobj=itxt)
            itxt.write("\n\n\n\n")
            print("\n\n")

if __name__ == '__main__':
    # set the config file working directory
    wkdir = str(Path(__file__).resolve().parent) + os.pathsep
    cl = RunStats(autorun=True)
