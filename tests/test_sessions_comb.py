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
from src import config as cfg
from src.sessions_comb import Sessions
import pytest

"""Unit tests for Sessions methods."""

def test_init(config_defaults):
    """test Sessions init"""
    sc = Sessions()
    assert len(sc.sessions) == cfg.n_sessions

@pytest.mark.skip(reason="build session runs too long")
def test_check_sess_attendees(config_defaults):
    """test check_sess_attendees"""
    print_cfg()
    sc = Sessions()
    good_session = [x for x in range(cfg.n_attendees)]    
    sc.build_sessions()
    # res_list = list(sc.sessions[1]) #.values()).sort()
    for k, v in sc.sessions.items():
        attnd_list = [e for i in v for e in i]
        attnd_list.sort()
        assert good_session == attnd_list

@pytest.mark.skip(reason="build sess runs too long")
def test_build_sessions(config_defaults):
    """ test build sessions"""
    print_cfg()

    # ss = group_items(cfg.attendees_list, cfg.group_size, cfg.sessions)
    # print(f" subsets: {len(ss)}")
    # print(ss)

    sc = Sessions()
    sc.build_sessions()
    print("test complete")

def print_cfg():
    """debug print of config variables"""
    print("\n\n****")
    print(f"   attendees: {cfg.n_attendees}")
    print(f"  group_size: {cfg.group_size}")
    print(f"    sessions: {cfg.n_sessions}")

    
