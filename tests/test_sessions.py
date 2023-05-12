#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_sessions_comb.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>
 
from src import config as cfg
from src.sessions import Sessions
import pytest

"""Unit tests for Sessions methods."""

def test_init(config_event_defaults):
    """test Sessions init"""
    sc = Sessions(autorun=False)
    assert len(sc.sessions) == 0

def test_load_algorithm(config_event_defaults):
    """test check_sess_attendees"""
    s = Sessions(autorun=False)    
    assert True == hasattr(s,'ac')

def test_load_algorithm_module_fails(config_event_defaults):
    """test sys exit for bad algorithm module"""
    cfg.sys_group_algorithm = "BadModule"
    with pytest.raises(SystemExit) as e_info:
        s = Sessions(autorun=False)
    assert e_info.type == SystemExit

def test_load_algorithm_class_fails(config_event_defaults):
    """test sys exit for bad algorithm module"""
    cfg.sys_group_algorithm_class = "BadClass"
    with pytest.raises(SystemExit) as e_info:
        s = Sessions(autorun=False)
    assert e_info.type == SystemExit
