#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  config.py
#     in each module, from src import config as cfg
#     access variables in this module as cfg.xxxxxx
# 
#     the breakout_groups.ini file is created in the data directory and can be modified
#     to reflect the number of groups, attendees size 
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>

import configparser
from pathlib import Path
import os

flnm = "breakout_groups.ini"
wkdir_path = None
wkdir = None
incdir = None
datadir = None

# event variables
attendees_list = []
n_attendees = 0
group_size = 0
n_groups = 0
n_sessions = 0
group_labels = []

# config obj
config = None

def init():
    """ on init, read the config file, if not found, write the default file"""
    global wkdir_path, wkdir, incdir, datadir, config

    # set the directories
    if wkdir is None:
        wkdir_path = Path(__file__).parent.parent.resolve()
        incdir = str(Path(__file__).resolve().parent) + os.sep
        wkdir = str(Path(incdir).resolve().parent) + os.sep
        datadir = str(Path(wkdir).resolve()) + os.sep + 'data' + os.sep

    config = configparser.ConfigParser(allow_no_value=True)
    config = read_config_file(config)

    set_event_variables(config)

    return config

def read_config_file(config):
    """read in the breakout_groups.ini file if exists or create it"""
    if Path(f"{datadir}{flnm}").is_file():
        config.read(f"{datadir}{flnm}") 
    else:
        config = set_default_config(config)
        config = write_ini(config)
        # remove comments from sections to be consistent with data from read
        remove_default_comments(config)
    return config

def set_default_config(config):
    """define the default config file """
    config['DEFAULT'] = {'attendees': 11, 
                         'group_size': 3,
                         'groups_per_session':3,
                         'sessions': 4,
                        }

    if not config.has_section('GROUP_LABELS'):
        config.add_section('GROUP_LABELS')                          
    config.set('GROUP_LABELS', '# list labels as session1 = label1,label2,label3...')
    config.set('GROUP_LABELS', '# labels can be different for each breakout session')
    config.set('GROUP_LABELS', '# if no sessions listed, default lable of group1, group2, ... will be used')
    config.set('GROUP_LABELS', 'session1', 'group1,group2,group3,group4,group5')
    config.set('GROUP_LABELS', 'session2', 'blue,red,green,yellow,pink')
    config.set('GROUP_LABELS', 'session3', 'Portales,Santa Fe,Taos,Chama,Cuba')
    config.set('GROUP_LABELS', 'session4', 'Elbert,Massive,Harvard,Blanca,La Plata')
                            
    return config

def remove_default_comments(config):
    """remove the comments set up in the defaults"""
    for s in config.sections():
        # the key is a tuple (key, value)
        for key in config[s].items(): 
            if key[0][:1] in config._comment_prefixes:
                config.remove_option(s, key[0])
    
def write_ini(config):
    """ write the ini file from the current cfg settings"""
    with open(f"{datadir}{flnm}", 'w') as configfile:
        config.write(configfile)
        
    return config
def set_event_variables(config):
    """set the event variables for consistant access"""
    global n_attendees, attendees_list, group_size, n_groups, n_sessions
    n_attendees = config.getint('DEFAULT','attendees')
    group_size = config.getint('DEFAULT','group_size')
    n_groups = config.getint('DEFAULT','groups_per_session')
    n_sessions = config.getint('DEFAULT','sessions')

    attendees_list = gen_attendees_list()
    global group_labels
    group_labels = build_group_labels()

def gen_attendees_list() -> list:
    """generate the list for attendees"""
    attendees_list = [x for x in range(n_attendees)]
    return attendees_list

def build_group_labels() -> list:
    """read group label dict and build a list of lists of the labels for each 
       group in a session
       this removes the key from the dict and does not force a naming convention 
       in the ini file
    """

    group_labels = []
    for k, v in config['GROUP_LABELS'].items():
        if k not in config['DEFAULT']:
            group_labels.append(v.split(','))

    return group_labels

def debug_print():
    print("")
    print(f"    wkdir: {wkdir}")
    print(f"  inc dir: {incdir}")
    print(f" data dir: {datadir}")
    print(f"file name: {flnm}")

    print(config.sections())
    print(config['GROUP_LABELS'])

    for key, val in config['GROUP_LABELS'].items():
        print(f"   {key}:{val}")

    # print("    ",config['DEFAULT']['num_members'])
    # print(dir(config))

config = init()

