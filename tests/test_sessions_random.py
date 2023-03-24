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
    assert len(sc.sessions) == cfg.sessions

def test_check_sess_attendees():
    """test check_sess_attendees"""
    good_session = [0,1,2,3,4,5,6,7,8]    
    sc.build_sessions()
    res_list = list(sc.sessions[1]) #.values()).sort()
    for k, v in sc.sessions.items():
        attnd_list = [e for i in v for e in i]
        attnd_list.sort()
        assert good_session == attnd_list

def test_build_sessions():
    """ test build sessions"""
    sc.build_sessions()
    assert len(sc.sessions) == cfg.sessions 



    
