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


def test_init():
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
    sc.sess_setup()
    sc.gen_group_combinations()
    assert exp_res1 == sc.comb_dict[0]

def test_update_sess_attendees(config_event_defaults, get_random_seed):
    """ test update of sess attendees"""
    del_group = [[0,1,2], [0,3,4]]
    exp_res1 = [3,4,5,6,7,8,9,10]
    exp_res2 = [5,6,7,8,9,10]
    sc = SessionsManual(get_random_seed)
    sc.sess_setup()
    sc.gen_group_combinations()
    sc.update_sess_attendees(1, del_group[0])
    assert sc.sess_attendees[1] == exp_res1
    sc.update_sess_attendees(1, del_group[1])
    assert sc.sess_attendees[1] == exp_res2

def test_create_sessions(config_event_defaults, get_random_seed):
    """ test create of all sessions from comb"""
    exp_res1 = [[0,3,4], [1,5,6],[2,7,8], [0,9,10]]
    sc = SessionsManual(get_random_seed)
    sc.sess_setup()
    sc.gen_group_combinations()
    sc.create_sessions()
    assert sc.sessions[0] == exp_res1

def test_create_sessions_extra_sessions(config_event_defaults, get_random_seed):
    """ test create sessions with large number of sessions"""
    cfg.n_sessions = 7
    exp_res1 = [[0,3,4], [1,5,6],[2,7,8], [0,9,10]]
    sc = SessionsManual(get_random_seed)
    sc.sess_setup()
    sc.gen_group_combinations()
    sc.create_sessions()
    assert sc.sessions[0] == exp_res1

@pytest.mark.skip("not valid test")
def test_update_card_interactions(config_event_defaults, get_random_seed):
    """ test update of interactions """
    sess = [[1, 3, 10, 8], [0, 6, 9], [4, 5, 7, 2]]
    sc = SessionsManual(get_random_seed)
    sc.update_card_interactions(sess)
    assert sc.all_cards[0].card_interactions[6] == 1
    assert sc.all_cards[0].card_interactions[9] == 1
    assert sc.all_cards[1].card_interactions[1] == 1
    assert sc.all_cards[1].card_interactions[10] == 1
    assert sc.all_cards[1].card_interactions[6] == 0
