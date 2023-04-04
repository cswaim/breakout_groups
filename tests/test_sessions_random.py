#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>
 
import pytest

from src import config as cfg
from src.sessions_random import Sessions 

"""Unit tests for Sessions methods."""


def test_init(config_defaults):
    """test Sessions init"""
    sc = Sessions()
    assert len(sc.sessions) == cfg.n_sessions

def test_check_sess_attendees(config_defaults):
    """test check_sess_attendees"""
    sc = Sessions()
    good_session = [x for x in range(cfg.n_attendees)]   
    sc.build_sessions()
    for k, v in sc.sessions.items():
        attnd_list = [e for i in v for e in i]
        attnd_list.sort()
        assert good_session == attnd_list

def test_build_sessions(config_defaults):
    """ test build sessions"""
    sc = Sessions()
    sc.build_sessions()
    assert len(sc.sessions) == cfg.n_sessions 



    
