#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  config.py
#     in each module, from src import config as cfg
#     access variables in this module as cfg.xxxxxx
#
#     the config file is created in the data directory and can be modified
#     for a specific run.
#
#  Copyright 2024 cswaim <cswaim@jcrl.net>
#  Licensed under the Apache License, Version 2.0
#  http://www.apache.org/licenses/LICENSE-2.0

# import this module as the first application module:
#     import src.config as cfg

# system variables change only the cfg_flnm
cfg_flnm = "breakout_groups.cfg"
wkdir_path = None
wkdir = None
srcdir = None
datadir = None

# event variables
event_title = "Test Event"
event_subtitle = ""
event_date = ""
n_attendees = 11
group_size = 3
n_groups = 3
n_sessions = 4
n_extra_cards = 2
random_seed = None
group_labels = [['group1,group2,group3,group4,group5'],
                ['blue,red,green,yellow,pink'],
                ['Portales,Santa Fe,Taos,Chama,Cuba'],
                ['Elbert,Massive,Harvard,Blanca,La Plata'],
               ]
session_ng_overrides = {}
session_labels = []

# reports
report_interactions_matrix = True
report_run_stats = True
report_cards = True

# system variables
sys_cfg_version = '0.10'
sys_comment_prefixes = ['#', ';']
sys_group_algorithm = "sessions_random"
sys_group_algorithm_class = "SessionsRandom"
sys_algorithm_compare = ["sessions_random","SessionsRandom",
        "sessions_random_interactions","SessionsRandomInteractions",
        ]
# output file names
sys_run_stats_csv = "run_stats.csv"
sys_run_stats_txt = "run_stats.txt"
sys_cards_pdf = "cards.pdf"
sys_cards_txt = "cards.txt"
sys_interactions_reports_txt = "interactions_reports.txt"

# values passed to ConfigParms
# dict key is the section, value is a list of variable names and type
#   types are i-integer, f-float, b-boolean, s-string, l-list

cfg_values = {'EVENT': [
                ('event_title', 's'), ('event_subtitle', 's'),
                ('event_date', 's'),
                ('n_attendees', 'i'),
                ('n_groups', 'i'), ('n_sessions', 'i'),
                ('n_extra_cards', 'i'),
                ('random_seed', 'i'),('session_labels', 'l'),
                ],
              'SESSION_NG_OVERRIDES' : {},
              'GROUP_LABELS': [],
              'REPORTS':[
                  ('report_interactions_matrix', 'b'),
                  ('report_run_stats', 'b'),
                  ('report_cards', 'b'),
              ],
              'SYSTEM': [
                ('sys_cfg_version', 's'),
                ('sys_comment_prefixes', 'l'),
                ('sys_group_algorithm', 's'),
                ('sys_group_algorithm_class', 's'),
                ('sys_algorithm_compare', 'l'),
                ('sys_run_stats_csv', 's'),
                ('sys_run_stats_txt', 's'),
                ('sys_cards_pdf', 's'),
                ('sys_cards_txt', 's'),
                ('sys_interactions_reports_txt', 's'),
                ],
             }
cfg_comments = {
    'event_title': ['event title, subtitle and date must be <= 30 characters'],
    'event_date': ['date is a string and will be printed as entered, examples:', 'YYYY/MM/DD, Jan 1 thru Jan 4, Sat Apr 5'],
    'group_size': ['if 0, group size is calculated, recommend 0',],
    'GROUP_LABELS': ['list labels as sess1 = label1,label2,label3...', 'labels can be different for each breakout session', 'if no session label is available, default labels of group1, group2, ... will be used', 'the session key must be unique but is ignored, only the values are used'],
    'SESSION_NG_OVERRIDES': ['the num of groups per session may be overidden by entering:', 'sess_num = integer', '3 = 6', 'session is 0 offset, so session1 is 0, session2 is 1'],
    'sys_cfg_version': ['changing the version number will cause file to be rewritten',],
    'random_seed': ['random_seed = <int> forces random to return same value for each run', 'normally should be: random_seed = None '],
    'session_labels': ['a common separated list of labels = Fri 9:00,Sat 10:00,Sat 1:00pm ', 'if empty Session xx will be generated for each session', 'if number of labels provided is less than number of sessions, ','then Session xx will be generated for missing sessions'],
    'sys_run_stats_csv': ['output files names'],
    'sys_algorithm_compare': ['format of this is module_name, class_name, module_name, class_name', ' The list is parsed into a list of lists (module,class), (module, class)']
             }

# config obj
config = None
cp = None
cu = None
# store orig n_groups to restore from if overridden
orig_n_groups = 0

# variables passed to all modules
attendees_list = []
sessions = {}
sessions_info = {}
all_card_interactions = {}
all_cards = []
algo_runtime = None

"""
This module takes advantage of Python's behavior of importing the module
the first time and for every import after the first, only a reference is passed.  The code is not re-executed.

There are several ways to instantiate the ConfigParm class which reads the
cfg file.  Pick an approach that you like.

Note that setting the autorun may effect tests as the defaults from the
config file are loaded and the test defaults must be reset.

to autorun on the first import:
    cp = ConfigParms(cfg_values, cfg_comments, autorun=True)

to control the run in your application, just instantiate the class in this module
    run_init()

and then in the application code, read the parm file:
    cfg.run()
"""

# the imports must be at end of the config module
#
# To override the behavior of ConfigParms
# such as change the path to data or scr directories
# or to modify the default behavior for a section or variable
# (1) make the modifications in the configparms_ext module
#
# the init will look for the configparms_ext module first and use it
# if it exists, otherwise it will use the package configparms module

def run_init():
    """run the init
        if the configparms_ext module exists, use it and is preferred
        otherwise the package configparms module is used
    """
    global cp, cu
    try:
        from src.configparms_ext import ConfigParmsExt as ConfigParms
    except Exception as e:
        # from app_config.configparms import ConfigParms
        import os
        print("Failed to import src.configparms_ext")
        print(f"path:  {os.getcwd()}")
        print(f"Error: {e}")
        exit()

    from src.configutils import ConfigUtils
    cp = ConfigParms(cfg_values, cfg_comments, autorun=False)
    cu = ConfigUtils()

def run():
    """read the config file & set values in module"""
    cp.run()

# instantiate the configparms module
run_init()