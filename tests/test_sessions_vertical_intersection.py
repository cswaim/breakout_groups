#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_sessions_random.py
#
#  Copyright 2023 cswaim <cswaim@tpginc.net>

import pytest

from src import config as cfg
from src.sessions_vertical_intersection import SessionsVerticalIntersection

"""Unit tests for Sessions methods."""

@pytest.mark.skip(reason="number of sessions is one greater than req sessiosns")
def test_init(config_event_defaults, get_random_seed):
    """test Sessions init"""
    cfg.n_attendees = 16
    cfg.n_groups = 4
    cfg.group_size = 4
    sc = SessionsVerticalIntersection(seed=get_random_seed, autorun=True)
    cfg.sessions = sc.sessions
    assert len(sc.sessions) == cfg.n_sessions

def test_check_sess_attendees(config_event_defaults, get_random_seed):
    """test for check_sess_attendees"""
    cfg.n_attendees = 16
    cfg.n_groups = 4
    cfg.group_size = 4
    sc = SessionsVerticalIntersection(seed=get_random_seed)
    good_session = [x for x in range(cfg.n_attendees)]
    sessions = sc.build_sessions()
    for k, v in sessions.items():
        attend_list = [e for i in v for e in i]
        attend_list.sort()
        assert attend_list == good_session

@pytest.mark.skip(reason="number of sessions is one greater than req sessiosns")
def test_run(config_event_defaults, get_random_seed):
    """ test build sessions"""
    cfg.n_attendees = 16
    cfg.n_groups = 4
    cfg.group_size = 4
    sc = SessionsVerticalIntersection(seed=get_random_seed)
    sc.run()
    assert len(sc.sessions) == cfg.n_sessions
