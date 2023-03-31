#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>
 
import itertools as it
from itertools import combinations
import random
import math
import copy
from src.sessions_comb import Sessions
import pytest

from src import config as cfg
 
"""Unit tests for Sessions methods."""
sc = Sessions()

def test_init():
    """test Sessions init"""
    assert len(sc.sessions) == cfg.n_sessions

def test_check_sess_attendees():
    """test check_sess_attendees"""
    good_session = [x for x in range(cfg.n_attendees)]    
    sc.build_sessions()
    # res_list = list(sc.sessions[1]) #.values()).sort()
    for k, v in sc.sessions.items():
        attnd_list = [e for i in v for e in i]
        attnd_list.sort()
        assert good_session == attnd_list


def test_build_sessions():
    """ test build sessions"""
    print("\n\n****")
    print(f"   attendees: {cfg.n_attendees}")
    print(f"  group_size: {cfg.group_size}")
    print(f"    sessions: {cfg.n_sessions}")

    # ss = group_items(cfg.attendees_list, cfg.group_size, cfg.sessions)
    # print(f" subsets: {len(ss)}")
    # print(ss)

    sc = Sessions()
    sc.build_sessions()
    print("test complete")



    
