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

# import this module as the first application module:
#     import src.config as cfg

import configparser
from pathlib import Path
import os

flnm = "breakout_groups.ini"
wkdir_path = None
wkdir = None
srcdir = None
datadir = None

# event variables
attendees_list = []
n_attendees = 11
group_size = 3
n_groups = 3
n_sessions = 4
group_labels = [['group1,group2,group3,group4,group5'],
                ['blue,red,green,yellow,pink'],
                ['Portales,Santa Fe,Taos,Chama,Cuba'],
                ['Elbert,Massive,Harvard,Blanca,La Plata'],
               ] 

# config obj
config = None

# system variables
sys_version = '0.1'
sys_group_algorithm = ""

def init():
    """ on init, read the config file, if not found, write the default file"""
    global wkdir_path, wkdir, srcdir, datadir, config

    # set the directories
    if wkdir is None:
        wkdir_path = Path(__file__).parent.parent.resolve()
        srcdir = str(Path(__file__).resolve().parent) + os.sep
        wkdir = str(Path(srcdir).resolve().parent) + os.sep
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

     # if the sys_version is different, write out the new config file
    if not config.has_option('SYSTEM', 'sys_version') or sys_version != config.get('SYSTEM', 'sys_version'):
        config = set_event_variables(config)
        config = set_default_config(config)
        config = write_ini(config)
    
    # remove comments from sections to be consistent with data from read
    remove_default_comments(config)
    return config

def set_default_config(config):
    """define the default config file """
    config['EVENT'] = {'n_attendees': n_attendees, 
                         'group_size': group_size,
                         'n_groups': n_groups,
                         'n_sessions': n_sessions,
                        }

    if not config.has_section('GROUP_LABELS'):
        config.add_section('GROUP_LABELS') 
    config["GROUP_LABELS"].clear()                         
    config.set('GROUP_LABELS', '# list labels as session1 = label1,label2,label3...')
    config.set('GROUP_LABELS', '# labels can be different for each breakout session')
    config.set('GROUP_LABELS', '# if no sessions listed, default lable of group1, group2, ... will be used')
    config.set('GROUP_LABELS', '# the session key must be unique but is ignored, only the values are used')
    for i, g in enumerate(group_labels):
        config.set('GROUP_LABELS', f'sess{i}', ','.join(x for x in g))

    if not config.has_section('SYSTEM'):
        config.add_section('SYSTEM')                          
    config.set('SYSTEM', 'sys_version', str(sys_version))
                            
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
    n_attendees = config.getint('EVENT','n_attendees')
    group_size = config.getint('EVENT','group_size')
    n_groups = config.getint('EVENT','n_groups')
    n_sessions = config.getint('EVENT','n_sessions')

    attendees_list = gen_attendees_list()
    global group_labels
    group_labels = build_group_labels()

    # system parameters
    # do not set the version from the file
    # global sys_xxx
    # sys_xxx = config.get('SYSTEM', 'xxx')

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
        if k not in config['EVENT']:
            group_labels.append(v.split(','))

    return group_labels

def debug_print():
    print("")
    print(f"    wkdir: {wkdir}")
    print(f"  inc dir: {srcdir}")
    print(f" data dir: {datadir}")
    print(f"file name: {flnm}")

    print(config.sections())
    print(config['GROUP_LABELS'])

    for key, val in config['GROUP_LABELS'].items():
        print(f"   {key}:{val}")

    # print("    ",config['DEFAULT']['num_members'])
    # print(dir(config))

config = init()

