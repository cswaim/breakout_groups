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
import math
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

def print_header(hd1, hd2=None, col_hd1=None, col_hd2=None, fmt="std", fileobj=None):
    """print report header
        fmt=std will use the template
        fmt=None will just print the hd1, hd2 as passed
        fileobj defaults to sys.stdout
    """
    # set date if not set
    if dt is None:
        set_rpt_date()

    print("", file=fileobj)
    # print report headers
    if fmt == "std":
        print(hd1_template.format(dt.strftime("%y-%m-%d"), hd1, dt.strftime("%H:%M:%S")), file=fileobj)
    else:
        print(f"{hd1}", file=fileobj)
    if hd2 is not None:
        if fmt == "std":
            print(hd2_template.format(hd2), file=fileobj)
        else:
            print(f"{hd2}", file=fileobj)

    # print column headings
    if col_hd1 is not None:
        print(col1_template.format(col_hd1), file=fileobj)
    if col_hd2 is not None:
        print(col2_template.format(col_hd2), file=fileobj)

def print_dtl(line, fileobj=None, newline=True):
    """print detail report line"""
    if newline:
        print(line, file=fileobj)
    else:
        print(line, end="", file=fileobj)

def print_event_parms_limited(fileobj=None):
    """ print the event parameters"""
    print_dtl("", fileobj)
    print_dtl(f"         attendees: {cfg.n_attendees}", fileobj)
    print_dtl(f"        group_size: {cfg.group_size}", fileobj)
    print_dtl(f"groups_per_session: {cfg.n_groups}", fileobj)
    print_dtl(f"          sessions: {cfg.n_sessions}", fileobj)
    print_dtl("", fileobj)

def calc_event_stats() -> dict:
    """calc the static event stats based on values in config file"""
    event_stats = {}
    # calc max group size
    q, r = divmod(cfg.n_attendees, cfg.n_groups)
    if r > 0:
        max_group_size = q + 1
    else:
        max_group_size = q
        cfg.group_size = q
    event_stats["max_group_size"] = max_group_size

    # the number of times the max group will occur in a session
    max_group_size_occurence = r
    event_stats["max_group_size_occurence"] = max_group_size_occurence

    # max num of interactions an individual can have
    max_idivi = (max_group_size - 1) * cfg.n_sessions
    event_stats["max_idivi"] = max_idivi

    # possible unique interactions possible n(n-1)/2
    pui = math.comb(cfg.n_attendees, 2)
    event_stats["pui"] = pui

    # max interactions is constrained by number of sessions
    def calc_group_int(n):
        """calc number of group interactions based on group size"""
        return int(((n-1)*n)/2)
    # calc the interations in session, accounting for diff group sizes
    sess_int = 0
    # calc interactions in oversize groups
    for x in range(max_group_size_occurence):
        sess_int += calc_group_int(max_group_size)
    # calc interactions in reg groups
    for x in range(cfg.n_groups - max_group_size_occurence):
        sess_int += calc_group_int(cfg.group_size)
    # now mult session int by number of sessions
    max_pi = sess_int * cfg.n_sessions
    event_stats["max_i"] = max_pi

    # possible combinations n! / r!(n-r)!    r is group size
    puc = math.comb(cfg.n_attendees, cfg.group_size)
    event_stats["puc"] = puc
    gc = cfg.n_sessions * cfg.n_groups
    event_stats["gc"] = gc

    return event_stats
