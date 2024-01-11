from pathlib import Path
import os
import io
import pandas as pd
import math
import csv
from datetime import datetime
from src import config as cfg
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
        self.ratio_tot_inter = 0
        self.unique_inter_cnt = 0
        self.ratio_unique_inter = 0
        self.miss_inter_cnt = 0

        self.calc_event_stats()

        if autorun:
            self.run()

    def calc_event_stats(self):
        """calc the event stats"""
        estats = rptu.calc_event_stats()

        # set the values from estats
        self.max_group_size = estats["max_group_size"]
        self.max_group_size_occurence = estats["max_group_size_occurence"]
        self.max_idivi = estats["max_idivi"]
        self.pui = estats["pui"]
        self.max_i = estats["max_i"]
        self.puc = estats["puc"]
        self.gc = estats["gc"]

    def gen_run_stats(self,):
        """ calc the stats for each run"""
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

        self.ratio_tot_inter = self.inter_cnt / self.pui
        self.unique_inter_cnt = self.inter_cnt - self.dup_inter_cnt
        self.ratio_unique_inter = self.unique_inter_cnt / self.pui
        # missed cnt is overstated
        self.miss_inter_cnt = self.pui - self.inter_cnt

        return df

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
        print(f"                 algoritim_runtime: {cfg.algo_runtime}", file=fileobj)
        print("", file=fileobj)
        print(f"attendees_list: {cfg.attendees_list}", file=fileobj)
        print("", file=fileobj)
        print(f"                         attendees: {cfg.n_attendees}", file=fileobj)
        print(f"                        group_size: {cfg.group_size}", file=fileobj)
        print(f"  max group_size (add'l attendees): {self.max_group_size}", file=fileobj)
        print(f"                groups_per_session: {cfg.n_groups}", file=fileobj)
        print(f"                          sessions: {cfg.n_sessions}", file=fileobj)
        print("", file=fileobj)
        print(f"                              seed: {cfg.random_seed}", file=fileobj)
        print("", file=fileobj)
        print(f"                Total Interactions: {self.inter_cnt}", file=fileobj)
        print(f"               Unique Interactions: {self.unique_inter_cnt}", file=fileobj)
        print(f"            Duplicate Interactions: {self.dup_inter_cnt}", file=fileobj)
        print(f"  Num missed/orphaned interactions: {self.miss_inter_cnt}", file=fileobj)
        print(f"      Possible Unique interactions: {self.pui}", file=fileobj)
        print(f"                  Max interactions: {self.max_i}", file=fileobj)
        print(f"       Max Individual interactions: {self.max_idivi}", file=fileobj)
        print(f"     Tot effective rate (tot/poss): {self.ratio_tot_inter:0.2}", file=fileobj)
        print(f" Unique effective rate (uniq/poss): {self.ratio_unique_inter:0.2}", file=fileobj)
        print("", file=fileobj)
        print(f"                group combinations: {self.gc}", file=fileobj)
        print(f"       Possible group combinations: {self.puc}", file=fileobj)

        """list the sessions"""
        print("\n\n", file=fileobj)
        for i, val in cfg.sessions.items():
            print(f"{cfg.session_labels[i]} - {val}", file=fileobj)

    def write_stats_csv(self,):
        """write stats to csv"""
        # no space between headings to support pandas load
        headers = "Date/Time,Algorithm,Algorithm_RunDur,Total_Interactions,Missed_Interactions,Duplicate_Interactions,Ratio_Interactions,Unique_Interactions,Ratio_Unique_Interactions,Event_Possible_Unique_Interactions,Max_Interactions,Max_IndivInt,Possible_Group_Combinations,Group_Combinations,Num_Attendees,Group_Size,Max_Group_Size,Num_Groups,Num_Sessions,Random_Seed\n"
        # headers="Date/Time,algorithm,algo_rt,tot_i,mis_i,dup_i,rti,uniq_i,rui,pui,max_i,max_indi,puc,tot_comb,n_attendees,group_size,n_groups,n_sessions,r_seed\n"

        dt_filter = '%Y-%m-%d %H:%M:%S'
        dtl = f'"{datetime.now().strftime(dt_filter)}", {cfg.sys_group_algorithm_class}, {cfg.algo_runtime.total_seconds()}, {self.inter_cnt}, {self.miss_inter_cnt}, {self.dup_inter_cnt}, {self.ratio_tot_inter}, {self.unique_inter_cnt}, {self.ratio_unique_inter}, {self.pui}, {self.max_i}, {self.max_idivi}, {self.puc}, {self.gc}, {cfg.n_attendees}, {cfg.group_size}, {self.max_group_size}, {cfg.n_groups}, {cfg.n_sessions}, {cfg.random_seed}\n'

        csvfl_path = Path(f'{cfg.datadir}{cfg.sys_run_stats_csv}')

        # if file does not exist, create it and write header
        if not csvfl_path.is_file():
            with open(csvfl_path, 'w') as new_csv:
                new_csv.write(headers)

        # append to file
        with open(csvfl_path, 'a', newline='') as csvfile:
           csvfile.write(dtl)

    def run(self,):
        with open(f'{cfg.datadir}{cfg.sys_run_stats_txt}', 'w') as itxt:
            # make file obj available to all methods
            self.itxt = itxt
            # calc the stats
            self.gen_run_stats()
            self.print_stats()
            self.print_stats( fileobj=itxt)
            itxt.write("\n\n\n\n")
            print("\n\n")
        self.write_stats_csv()

if __name__ == '__main__':
    # set the config file working directory
    wkdir = str(Path(__file__).resolve().parent) + os.pathsep
    cfg.cp.run()
    cl = RunStats(autorun=True)
