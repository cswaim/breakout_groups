#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_sessions_algo.py
#
#  Copyright 2023 cswaim <cswaim@tpginc.net>

import pytest

from src import config as cfg
from src.sessions_algo import SessionsAlgo

"""Unit tests for Sessions methods."""


def test_init(get_random_seed):
    """test Sessions init"""
    sa = SessionsAlgo(seed=get_random_seed, autorun=True)
    assert len(sa.sessions) == cfg.n_sessions

def test_check_sess_attendees(config_event_defaults, get_random_seed):
    """test for check_sess_attendees"""
    sa = SessionsAlgo(seed=get_random_seed)
    # good_session = [x for x in range(cfg.n_attendees)]
    good_session = {0:[[1,2,3,11],[4,5,6],[7,8,9,10]],
                    1:[[1,4,7,8,10],[2,5,11,12],[3,6,9,13]],
                    2:[[1,5,9],[2,4,7],[3,6,8,10]],
                    3:[[2,4,6,8],[0,1,7,10],[3,5,9]],
                    }
    sessions = sa.build_sessions()
    sa.sessions = sa.check_num_groups(sessions)

    for k, v in sa.sessions.items():
        #attend_list = [e for i in v for e in i]
        #attend_list.sort()
        assert v == good_session[k]


def test_build_sessions(config_event_defaults, get_random_seed):
    """ test build sessions"""
    sa = SessionsAlgo(seed=get_random_seed)
    sessions = sa.build_sessions()
    assert len(sessions) == cfg.n_sessions
