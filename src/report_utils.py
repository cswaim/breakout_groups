#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  report_utilities.py
#
#  Copyright 2023 cswaim <cswaim@jcrl.net>

"""
    Common routines used by the reporting modules

    from src import report_utils as rptu
"""

from datetime import datetime
from src import config as cfg

dt = None
hd1_template = """ Date: {} {:^50} Time: {}"""
hd2_template = """             {:^50} """

col1_template = """ {}"""
col2_template = """ {}"""

def set_rpt_date(rpt_date=None):
    """set the report date"""
    global dt
    if rpt_date is None:
        dt = datetime.now()
    else:
        dt = rpt_date

def print_header(hd1, hd2=None, col_hd1=None, col_hd2=None,fmt="std"):
    """print report header"""
    if dt is None:
        set_rpt_date()
    print("")
    if fmt == "std":
        print(hd1_template.format(dt.strftime("%y-%m-%d"), hd1, dt.strftime("%H:%M:%S")))
    else:
        print(f"{hd1_template}")
    if hd2 is not None:
        print(hd2_template.format(hd2))

    if col_hd1 is not None:
        print(col1_template.format(col_hd1))
    if col_hd2 is not None:
        print(col2_template.format(col_hd2))

def print_dtl(line):
    """print detail report line"""
    print(line)
