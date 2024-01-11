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
        custom_hd = ["Date/Time","algorithm","algo_rt","tot_i","mis_i","dup_i","rti","uniq_i","rui","pui","max_pi","max_indi","puc","tot_comb","n_attendees","group_size","mgroup_size","n_groups","n_sessions","rand_seed"]
        csvfl_path = Path(f'{cfg.datadir}{cfg.sys_run_stats_csv}')
        # self.df = pd.read_csv(csvfl_path)
        self.df = pd.read_csv(csvfl_path, header=None, names=custom_hd, skiprows=1)

    def find_best_ratio(self,):
        """ sort the df by unique interactions ratio
            select the top 3 for each module
            return answer set df
        """
        # Date/Time,Algorithm,Algorithm_Runtime,Interactions,Missed_Interactions,Duplicate_Interactions,Interaction_Ratio,Unique_Interactions,Interaction_Ratio_Unique,Event_Possible_Unique_Interactions,Max_Possible_Unique_Interactions,Max_idivi,Possible_Group_Combinations,Group_Combinations,Num_Attendees,Group_Size,Num_Groups,Num_Sessions,Random_Seed

        #headers="Date/Time,algorithm,algo_rt,tot_i,mis_i,dup_i,rti,uniq_i,rui,pui,max_pui,max_indi,puc,tot_comb,n_attendees,group_size,mgroup_size,n_groups,n_sessions,r_seed\n"

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
        print("rui is Actual Unique Interactions/ Possible Unique Interactions")
        print("rti is Actual  Interactions/ Possible Unique Interactions")
        print("")

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
