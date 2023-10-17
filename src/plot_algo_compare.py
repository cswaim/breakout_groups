from pathlib import Path
import os
import io
import pandas as pd
import matplotlib.pyplot as plt

from src import config as cfg


class PlotAlgoCompare():
    """ plot the results of the RunStats csv file"""

    def __init__(self, autorun=False):
        """init module """
        self.df = None

        if autorun:
            self.run()

    def build_plot_file_name(self, plot_id='') -> str:
        """build unique plot file names if id is passed"""
        if plot_id != "":
            plot_id = f'_{plot_id}'
        plot_pdf_path = Path(f'{cfg.datadir}plot_rs{plot_id}.pdf')
        return plot_pdf_path

    def plot_unique_interactions(self, ):
        """ plot the unique interactions for each run"""
        plot_path = self.build_plot_file_name(plot_id="ui")
        plt.title("Unique Interactions")
        # define the index column (x axis)
        self.df.set_index('Date/Time',inplace=True)
        # group by alogrithm
        self.df.groupby('Algorithm')['Unique_Interactions'].plot(legend=True)

        # plot it
        plt.savefig(plot_path)


    def run(self,):
        # build the full path to csv file
        csvfl_path = Path(f'{cfg.datadir}run_stats.csv')
        self.df = pd.read_csv(csvfl_path)
        print(self.df)

        self.plot_unique_interactions()


if __name__ == '__main__':
    # set the config file working directory
    wkdir = str(Path(__file__).resolve().parent) + os.pathsep
    pac = PlotAlgoCompare(autorun=True)
