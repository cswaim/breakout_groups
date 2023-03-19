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
    
    # if Path(f"{datadir}{flnm}").is_file():
    #     config.read(f"{datadir}{flnm}") 
    # else:
    #     config = set_default_config(config)
    #     config = write_ini(config)
    #     # remove comments from sections to be consistent with data from read
    #     remove_default_comments(config)
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
    config['DEFAULT'] = {'attendees': 30,
                         'group_size': 6,
                         'groups_per_session': 5,
                         'sessions': 3,

                        }
    # config['GROUP_LABELS'] = {'# list labels as session1 = label1,label2,label3...':'',
    #                           '# labels can be different for each breakout session',
    #                           '# if no sessions listed, default lable of group1, group2, ... will be used',

    if not config.has_section('GROUP_LABELS'):
        config.add_section('GROUP_LABELS')                          
    config.set('GROUP_LABELS', '# list labels as session1 = label1,label2,label3...')
    config.set('GROUP_LABELS', '# labels can be different for each breakout session')
    config.set('GROUP_LABELS', '# if no sessions listed, default lable of group1, group2, ... will be used')
    config.set('GROUP_LABELS', 'session1', 'group1,group2,group3,group4,group5')
    config.set('GROUP_LABELS', 'session2', 'group1,group2,group3,group4,group5')
                            
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

