#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>
 
from src.sessions_random import Sessions
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
    for k, v in sc.sessions.items():
        attnd_list = [e for i in v for e in i]
        attnd_list.sort()
        assert good_session == attnd_list

def test_build_sessions():
    """ test build sessions"""
    sc.build_sessions()
    assert len(sc.sessions) == cfg.n_sessions 



    
