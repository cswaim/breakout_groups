#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  logger_setup.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>
 

import datetime
import logging
import logging.config
from pathlib import Path
import src.logger_filters             # referenced in yaml file
import yaml
from src import config as cfg

log = logging.getLogger('debug_logger')

# custom level for logging to console and not file
INFOCON = 25

def dict_config(config):
    """config the logging module"""
    logging.config.dictConfigClass(config).configure()

def create_logger():
    """ get the logger and return"""
    return logging.getLogger('debug_logger')

def fmt_file_name_init(config):
    """ add data dir to the fileHandler filenames"""
    # set date_time same for all log files
    dt = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_classes = ['logging.FileHandler', 'logging.handlers.RotatingFileHandler', ]
    for hdlr in config['handlers'].items(): 
        hname = hdlr[0]
        hdata = hdlr[1]
        if hdata['class'] in file_classes:
            # a = hdata['filename'].split('.')
            # hdlr[1]['filename'] = f"{cfg.datadir}{a[0]}_{dt}_0.{a[1]}"
            hdlr[1]['filename'] = f"{cfg.datadir}{hdata['filename']}" 
            #ls.config['handlers']['file']['filename'] = hdlr.baseFilename

def fmt_file_name_incr(config, cnt=0):
    """ increment the counter in the fileHandler filenames"""
    # set date_time same for all log files
    file_classes = ['logging.FileHandler', 'logging.handlers.RotatingFileHandler', ]
    for hdlr in config['handlers'].items(): 
        hname = hdlr[0]
        hdata = hdlr[1]
        if hdata['class'] in file_classes:
            a = hdata['filename'].split('.')
            ci = a[0].rfind('_')
            a[0] = a[0][:ci]
            hdlr[1]['filename'] = f"{cfg.datadir}{a[0]}_{cnt}.{a[1]}" 
            #ls.config['handlers']['file']['filename'] = hdlr.baseFilename


def infocon(self, msg, *args, **kwargs):
    """setup custom log level"""
    if self.isEnabledFor(INFOCON):
        self._log(INFOCON, msg, args, **kwargs)

def run():
    """set up the logger and return the logger object"""
    # set the current working directory - to get the source
    cwkdir = str(Path(__file__).resolve().parent) 

    # Load the config file
    with open(Path(cwkdir, "logger.yaml"), 'rt', encoding='utf8') as f:
        config = yaml.safe_load(f.read())

    # Configure the logging module with the config file
    fmt_file_name_init(config)
    dict_config(config)

    # logging.config.fileConfig('sample_log2.conf')

    # add custom level
    logging.addLevelName(INFOCON, 'INFOCON')

    logging.infocon = infocon
    logging.Logger.infocon = infocon

    # preformance tweaks - turn off functions not used by logger
    # Thread information
    logging.logThreads = False
    # process ID (os.getpid())
    logging.logProcesses = False
    # Current process name when using multiprocessing to manage multiple processes.
    logging.logMultiprocessing = False

    # create logger
    # log = create_logger()
    return 
