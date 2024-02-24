from pathlib import Path
import os
import io
import pandas as pd

from src import config as cfg
from src import reports_util as rptu

class AlgoCompareAnalysis():
    """ Analyze the results of the bg_algo_compare run

        identify the most effective solution based on ratio of
        unique interactions
    """

    def __init__(self, autorun=False):
        """init module """
        self.df = None
        self.df_res = None

        if autorun:
            self.run()

    def build_dataframe(self,):
        """build the panadas dataframe from the run stats csv"""
        csvfl_path = Path(f'{cfg.datadir}{cfg.sys_run_stats_csv}')

        # load csv and use custom column names by renaming columns
        # rename continues to work as ne columns are added to csv
        custom_cols = {"Algorithm": "algorithm", "Algorithm_RunDur": "algo_rt", "Unique_Interactions": "uniq_i", "Missed_Interactions": "mis_i",  "Duplicate_Interactions": "dup_i", "Ratio_Interactions": "rti", "Ratio_Unique_Interactions": "rui", "Event_Possible_Unique_Interactions": "pui", "Max_Interactions": "max_pi", "Max_IndivInt": "max_indi", "Possible_Group_Combinations": "puc", "Group_Combinations": "tot_comb", "Num_Attendees": "n_attendees", "Group_Size": "group_size", "Max_Group_Size": "mgroup_size", "Num_Groups": "n_groups", "Num_Sessions": "n_sessions", "Num_Extra_Cards": "n_extra_cards", "Random_Seed": "rand_seed"}
        self.df = pd.read_csv(csvfl_path)
        self.df.rename(custom_cols, axis='columns', inplace=True)

    def find_best_ratio(self,):
        """ sort the df by unique interactions ratio
            select the top 3 for each module
            return answer set df
        """

        # get the top 3 for each algorithm
        df_res = self.df.sort_values(by=['algorithm', 'rui'],
        ascending=[True, False]).groupby('algorithm').head(3)
        # sort by ratio
        df_res.sort_values(by=['rui'],ascending=[False], inplace=True)
        self.df_res = df_res

    def print_results(self):
        """print the results from the df"""
        # get event statastics
        estats = rptu.calc_event_stats()

        print(f"                    Max Group Size (overflow): {estats['max_group_size']}")
        print(f"         Max Group Size Occurence per Session: {estats['max_group_size_occurence']}")
        print(f"              Event Total Unique Interactions: {estats['pui']}")
        print(f"                       Event Max Interactions: {estats['max_i']}")
        print("")
        print("  rui is Unique Interactions/ Event Total Unique Interactions")
        print("  rti is Unique Interactions/ Event Max Interactions")


        # set max column width
        pd.set_option('display.max_colwidth', 20)

        print(self.df_res[['algorithm', 'uniq_i', 'mis_i', 'dup_i', 'rti', 'rui', 'rand_seed']])

    def run(self,):
        """ run the analysis"""
        self.build_dataframe()
        self.find_best_ratio()
        self.print_results()


# to run analysis standalone
if __name__ == '__main__':
    # set the config file working directory
    wkdir = str(Path(__file__).resolve().parent) + os.pathsep
    # build the full path to csv file only when running standalone
    cfg.sys_run_stats_csv = "run_stats_compare.csv"
    aca = AlgoCompareAnalysis(autorun=True)
