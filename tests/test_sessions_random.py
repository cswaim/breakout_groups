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


def test_init():
    """test Sessions init"""
    sc = Sessions()
    assert len(sc.sessions) == cfg.n_sessions


@pytest.mark.skip(reason="Need to refactor this test")
def test_check_sess_attendees(get_config):
    """test for check_sess_attendees"""
    config_values = get_config
    sc = Sessions()
    good_session = [x for x in range(config_values['attendees'])]
    sc.build_sessions()
    for k, v in sc.sessions.items():
        attend_list = [e for i in v for e in i]
        attend_list.sort()
        assert attend_list in good_session


def test_build_sessions(config_defaults):
         
    """ test build sessions"""
    sc = Sessions()
    sc.build_sessions()
    assert len(sc.sessions) == cfg.n_sessions 
