from pathlib import Path
import os
import io
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from src import config as cfg

class PlotAlgoCompare():
    """ plot the results of the RunStats csv file"""

    def __init__(self, autorun=False):
        """init module """
        self.df = None
        self.pp = None   # generic pdf pages plot
        self.pdf_obj_list = []

        if autorun:
            self.run()

    def create_pdf_obj(self, plot_id="") -> object:
        """create a output file object for pdf plots"""
        plot_name = self.build_plot_file_name(plot_id)
        pp =PdfPages(plot_name)
        # register object pdf pages for close loop
        self.pdf_obj_list.append(pp)
        return pp

    def build_plot_file_name(self, plot_id='') -> str:
        """build unique plot file names if id is passed"""
        if plot_id != "":
            plot_id = f'_{plot_id}'
        plot_pdf_path = Path(f'{cfg.datadir}plot_rs{plot_id}.pdf')
        return plot_pdf_path

    def plot_unique_interactions(self, ):
        """ plot the unique interactions for each run"""
        #plot_path = self.build_plot_file_name(plot_id="ui")
        uiplot = plt.figure("ui")
        uiplot.suptitle("Unique Interactions")
        # define the index column (x axis)
        self.df.set_index('Date/Time',inplace=True)
        # group by alogrithm
        self.df.groupby('Algorithm')['Unique_Interactions'].plot(legend=True)

        # plot it
        #plt.savefig(plot_path)
        self.pp.savefig(uiplot)

    def plot_missed_interactions(self, ):
        """ plot the missed interactions for each run"""
        miplot = plt.figure("mi")
        miplot.suptitle("Missed Interactions")
        # define the index column (x axis)
        #self.df.set_index('Date/Time',inplace=True)
        # group by alogrithm
        self.df.groupby('Algorithm')['Missed_Interactions'].plot(legend=True)

        # plot it
        self.pp.savefig(miplot)

    def plot_runtime(self, ):
        """ plot the run time for each algorithm"""
        plotpdf = self.create_pdf_obj(plot_id="rt")
        rtplot = plt.figure("rt")
        rtplot.suptitle("Algorithm Run Time")
        # define the index column (x axis)
        #self.df.set_index('Date/Time',inplace=True)
        # group by alogrithm
        self.df.groupby('Algorithm')['Algorithm_Runtime'].plot(legend=True)

        # plot it
        plotpdf.savefig(rtplot)


    def run(self,):
        # build the full path to csv file
        csvfl_path = Path(f'{cfg.datadir}run_stats.csv')
        self.df = pd.read_csv(csvfl_path)
        print(self.df)
        self.pp = self.create_pdf_obj()

        self.plot_unique_interactions()
        self.plot_missed_interactions()
        self.plot_runtime()

        # close open pdf files
        for pdf_obj in self.pdf_obj_list:
            pdf_obj.close()


if __name__ == '__main__':
    # set the config file working directory
    wkdir = str(Path(__file__).resolve().parent) + os.pathsep
    pac = PlotAlgoCompare(autorun=True)
