#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  reports_interactions_matrix.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>

from pathlib import Path
import os
import pandas as pd
import numpy as np
import seaborn as sns
from src import config as cfg

class InteractionsMatrix():
    """ produce the interactions matrix and write to data folder """ 

    def __init__(self, autorun=False):
        """init interactions matrix report"""
        self.all_interactions = self.build_interactions()
        if autorun:
            self.run()

    def build_interactions(self,):
        """create interactions dic with all counts"""
        #""" convert interactions counter to list"""
        # interactions = []
        # for k, v in cfg.all_card_interactions.items():
        #     ia = []
        #     for i in range(cfg.n_attendees):
        #         ia.append(f"{i}:{v[i]}")
        #     interactions.append([k,ia])
        #     #print(f"{k}:  {ia}") 
        # return interactions
        interactions = {}
        for k, v in cfg.all_card_interactions.items():
            #ia = {}
            ia = []
            for i in range(cfg.n_attendees):
                # ia[i] = v[i]
                ia.append(v[i])
            interactions[k] = ia
        return interactions

    def gen_matrix(self,):
        
        df = pd.DataFrame.from_dict(self.all_interactions)

        # set the lower half of df to 0
        for i, row in df.iterrows():
            # set diagonal to zero
            df.iloc[i, i] = 0
            # set lower half to zero
            for c in range(0, i):
                df.iloc[i,c] = 0
        
        print("=================")
        df=df.replace(0,"")

        print(df)
        print("=================")
        # index = df.index
        # index.name = "id"

        cm=sns.color_palette("coolwarm", as_cmap=True)
            
        df=df.replace(0,np.NaN)
        df.style.background_gradient(cmap=cm,vmin=0,vmax=cfg.group_size).highlight_null('black')
        # print(df)

    def run(self,):
        self.gen_matrix()
 
 
if __name__ == '__main__':
    # set the config file working directory
    wkdir = str(Path(__file__).resolve().parent) + os.pathsep
    cl = InteractionsMatrix()