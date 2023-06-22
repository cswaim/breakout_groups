#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_sessions_random.py
#
#  Copyright 2023 cswaim <cswaim@tpginc.net>

import pytest

from src import config as cfg
from src.sessions_random_interactions import SessionsRandomInteractions

"""Unit tests for Sessions methods."""


def test_init():
    """test Sessions init"""
    sc = SessionsRandomInteractions(autorun=True)
    assert len(sc.sessions) == cfg.n_sessions


def test_check_sess_attendees(config_event_defaults):
    """test for check_sess_attendees"""
    sc = SessionsRandomInteractions()
    good_session = [x for x in range(cfg.n_attendees)]
    sc.build_sessions()
    for k, v in sc.sessions.items():
        attend_list = [e for i in v for e in i]
        attend_list.sort()
        assert attend_list == good_session


def test_build_sessions(config_event_defaults):
    """ test build sessions"""
    sc = SessionsRandomInteractions()
    sc.build_sessions()
    assert len(sc.sessions) == cfg.n_sessions
