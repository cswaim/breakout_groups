#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_sessions_random.py
#
#  Copyright 2023 cswaim <cswaim@tpginc.net>

import pytest

from src import config as cfg
from src.sessions_random import SessionsRandom

"""Unit tests for Sessions methods."""

def test_init():
    """test Sessions init"""
    sc = SessionsRandom(autorun=True)
    assert len(sc.sessions) == cfg.n_sessions

def test_check_sess_attendees(config_event_defaults):
    """test for check_sess_attendees"""
    sc = SessionsRandom()
    good_session = [x for x in range(cfg.n_attendees)]
    sc.build_sessions()
    for k, v in sc.sessions.items():
        attend_list = [e for i in v for e in i]
        attend_list.sort()
        assert attend_list == good_session

def test_build_sessions(config_event_defaults):
    """ test build sessions"""
    sc = SessionsRandom()
    sc.build_sessions()
    assert len(sc.sessions) == cfg.n_sessions

def test_n_group_override(config_event_defaults):
    """ test n_group override withbuild sessions"""
    cfg.session_ng_overrides[1] = 5
    sc = SessionsRandom()
    sc.build_sessions()
    assert len(sc.sessions[1]) == 6