#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_sessions_random.py
#
#  Copyright 2023 cswaim <cswaim@tpginc.net>

import pytest

from src import config as cfg
from src.sessions_manual import SessionsManual

"""Unit tests for Sessions methods."""


def test_init(config_event_defaults, get_random_seed):
    """test Sessions init"""
    sc = SessionsManual(autorun=True)
    assert len(sc.sessions) == cfg.n_sessions

def test_build_sessions(config_event_defaults, get_random_seed):
    """test build_sessions for valid sessions"""
    sc = SessionsManual(get_random_seed)
    good_session = [x for x in range(cfg.n_attendees)]
    sc.build_sessions()
    # each session must include attendees
    for k, v in sc.sessions.items():
        attend_list = [e for i in v for e in i]
        attend_list.sort()
        assert attend_list == good_session
    # build all sessions
    assert len(sc.sessions) == cfg.n_sessions

def test_sess_setup(config_event_defaults, get_random_seed):
    """ test build sessions"""
    sc = SessionsManual(get_random_seed)
    sc.sess_setup()
    assert len(sc.sessions) == cfg.n_sessions

def test_gen_group_combinations(config_event_defaults,get_random_seed):
    """ test the building of the group combinations"""
    exp_res1 = [[0,1,2], [0,3,4], [0,5,6], [0,7,8]]
    exp_res2 = [[1,2,3], [1,4,5], [1,6,7], [1,8,9]]
    sc = SessionsManual(get_random_seed)
    # sc.sess_setup()
    sc.gen_group_combinations()
    assert exp_res1 == sc.comb_dict[0]

def test_update_sess_attendees(config_event_defaults, get_random_seed):
    """ test update of sess attendees"""
    del_group = [[0,1,2], [0,3,4]]
    exp_res1 = [3,4,5,6,7,8,9,10]
    exp_res2 = [5,6,7,8,9,10]
    sc = SessionsManual(get_random_seed)
    # sc.sess_setup()
    sc.gen_group_combinations()
    sc.update_sess_attendees(1, del_group[0])
    assert sc.sess_attendees[1] == exp_res1
    sc.update_sess_attendees(1, del_group[1])
    assert sc.sess_attendees[1] == exp_res2

def test_create_sessions(config_event_defaults, get_random_seed):
    """ test create of all sessions from comb"""
    exp_res1 = [[0,1,2],[3,4,5], [6,7,8]]
    sc = SessionsManual(get_random_seed)
    # sc.sess_setup()
    sc.gen_group_combinations()
    sc.create_sessions()
    assert sc.sessions[0] == exp_res1

@pytest.mark.skip("later")
def test_create_sessions_extra_sessions(config_event_defaults, get_random_seed):
    """ test create sessions with large number of sessions"""
    cfg.n_sessions = 7
    exp_res1 = [[0,3,4], [1,5,6],[2,7,8], [0,9,10]]
    sc = SessionsManual(get_random_seed)
    # sc.sess_setup()
    sc.gen_group_combinations()
    sc.create_sessions()
    assert sc.sessions[0] == exp_res1

def test_build_first_group(config_event_defaults, get_random_seed):
    """ test create of all sessions from comb"""
    exp_res0 = [[0,1,2]]
    exp_res2 = [[0,5,6]]
    sc = SessionsManual(get_random_seed)
    # sc.sess_setup()
    sc.gen_group_combinations()
    sc.build_first_group()
    assert sc.sessions[0] == exp_res0
    assert sc.sessions[2] == exp_res2

@pytest.mark.skip("later")
def test_build_missing_groups(config_event_defaults, get_random_seed):
    """ test create of all sessions from comb"""
    # test cannot contain 0
    exp_res1 = [[0,3,4], [1,5,6],[2,7,8], [0,9,10]]
    sc = SessionsManual(get_random_seed)
    # sc.sess_setup()
    sc.gen_group_combinations()
    sc.build_first_group()
    sc.build_missing_groups(1, [1, 4, 5])
    assert sc.sessions[0] == exp_res1

def test_run(config_event_defaults, get_random_seed):
    """ test update of interactions """
    sess1 = [[0,3,4], [1,6,7], [5,8,9]]
    sc = SessionsManual(get_random_seed)
    sc.run()
    assert sc.sessions[1] == sess1

