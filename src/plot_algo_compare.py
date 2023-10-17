from pathlib import Path
import os
import io
import pandas as pd
import math
import csv
from datetime import datetime
from src import config as cfg
from src import reports_util as rptu

class PlotAlgoCompare():
    """ plot the results of the RunStats csv file"""

    def __init__(self, autorun=False):
        """init module """

        if autorun:
            self.run()

    def run(self,):
        # build the full path to csv file
        csvfl_path = Path(f'{cfg.datadir}run_stats.csv')


if __name__ == '__main__':
    # set the config file working directory
    wkdir = str(Path(__file__).resolve().parent) + os.pathsep
    cl = PlotAlgoCompare(autorun=True)
