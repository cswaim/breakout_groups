from pathlib import Path
import os
import io
import pandas as pd

from src import config as cfg

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
        self.df = pd.read_csv(csvfl_path)

    def find_best_ratio(self,):
        """ sort the df by unique interactions ratio
            select the top 3 for each module
            return answer set df
        """
        # Date/Time,Algorithm,Algorithm_Runtime,Interactions,Missed_Interactions,Duplicate_Interactions,Interaction_Ratio,Unique_Interactions,Interaction_Ratio_Unique,Event_Possible_Unique_Interactions,Max_Possible_Unique_Interactions,Max_idivi,Possible_Group_Combinations,Group_Combinations,Num_Attendees,Group_Size,Num_Groups,Num_Sessions,Random_Seed
        df_res = self.df.sort_values(by=['Algorithm', 'Interaction_Ratio_Unique'], ascending=[True, False]).groupby('Algorithm').head(3)
        self.df_res = df_res

    def print_results(self):
        """print the results from the df"""
        #
        max_ratio = self.df_res.iloc[0]['Max_idivi'] / self.df_res.iloc[0]['Max_Possible_Unique_Interactions']
        print(f"max individual uniq inter: {self.df_res.iloc[0]['Max_idivi']}")
        print(f"The maxium unique interactions for this event is {self.df_res.iloc[0]['Max_Possible_Unique_Interactions']}")
        print(f"With the constraints of the number of sessions, the best possible ration is {max_ratio:0.2}")
        print(self.df_res[['Algorithm', 'Interaction_Ratio_Unique', 'Unique_Interactions',  'Interactions',]]) # 'Random_Seed']])

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
