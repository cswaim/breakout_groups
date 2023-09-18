#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_sessions_random.py
#
#  Copyright 2023 cswaim <cswaim@tpginc.net>

import pytest

from src import config as cfg
from src.sessions_comb import SessionsComb

"""Unit tests for Sessions methods."""


def test_init(config_event_defaults, get_random_seed):
    """test Sessions init"""
    sc = SessionsComb(autorun=True)
    assert len(sc.sessions) == cfg.n_sessions

def test_sess_setup(config_event_defaults, get_random_seed):
    """ test build sessions"""
    sc = SessionsComb(get_random_seed)
    sc.sess_setup()
    assert len(sc.sessions) == cfg.n_sessions

def test_gen_group_combinations(config_event_defaults,get_random_seed):
    """ test the building of the group combinations"""
    exp_res1 = [[0,1,2], [0,3,4], [0,5,6], [0,7,8]]
    exp_res2 = [[1,2,3], [1,4,5], [1,6,7], [1,8,9]]
    sc = SessionsComb(get_random_seed)
    # sc.sess_setup()
    sc.gen_group_combinations()
    assert exp_res1 == sc.comb_dict[0]

def test_update_sess_attendees(config_event_defaults, get_random_seed):
    """ test update of sess attendees"""
    del_group = [[0,1,2], [0,3,4]]
    exp_res1 = [3,4,5,6,7,8,9,10]
    exp_res2 = [5,6,7,8,9,10]
    sc = SessionsComb(get_random_seed)
    # sc.sess_setup()
    sc.gen_group_combinations()
    sc.update_sess_attendees(1, del_group[0])
    assert sc.sess_attendees[1] == exp_res1
    sc.update_sess_attendees(1, del_group[1])
    assert sc.sess_attendees[1] == exp_res2

def test_create_sessions(config_event_defaults, get_random_seed):
    """ test create of all sessions from comb"""
    exp_res1 = [[0,1,2,10],[3,4,5], [6,7,8,9]]
    sc = SessionsComb(get_random_seed)
    # sc.sess_setup()
    sc.gen_group_combinations()
    sc.create_sessions()
    assert sc.sessions[0] == exp_res1

def test_create_sessions_extra_sessions(config_event_defaults, get_random_seed):
    """ test create sessions with large number of sessions"""
    cfg.n_sessions = 7
    exp_res0 = [[0, 1, 2, 10], [3, 4, 5], [6, 7, 8, 9]]
    exp_res6 = [[1, 6, 7], [0, 3, 4, 7, 10], [5, 8, 9, 2]]
    sc = SessionsComb(seed=get_random_seed)
    # sc.sess_setup()
    sc.gen_group_combinations()
    sc.create_sessions()
    assert sc.sessions[0] == exp_res0
    assert sc.sessions[6] == exp_res6

def test_build_first_group(config_event_defaults, get_random_seed):
    """ test build of first group"""
    exp_res0 = [[0,1,2]]
    exp_res2 = [[0,5,6]]
    sc = SessionsComb(get_random_seed)
    # sc.sess_setup()
    sc.gen_group_combinations()
    sc.build_first_group()
    assert sc.sessions[0] == exp_res0
    assert sc.sessions[2] == exp_res2

def test_build_missing_groups(config_event_defaults, get_random_seed):
    """ test create of all sessions from comb"""
    # test cannot contain 0
    exp_res1 = [[0,3,4], [1,5,6], ]   #[2,7,8], [0,9,10]]
    sc = SessionsComb(get_random_seed)
    # sc.sess_setup()
    sc.gen_group_combinations()
    sc.build_first_group()
    sc.build_missing_groups(1, [1, 5, 6])
    assert sc.sessions[0] == exp_res1

def test_run(config_event_defaults, get_random_seed):
    """ test update of interactions """
    sess1 = [[0,3,4,2], [1,6,7], [5,8,9,10]]
    sc = SessionsComb(get_random_seed)
    sc.run()
    assert sc.sessions[1] == sess1

