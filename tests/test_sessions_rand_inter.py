#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_sessions_random.py
#
#  Copyright 2023 cswaim <cswaim@tpginc.net>

import pytest

from src import config as cfg
from src.sessions_rand_inter import SessionsRandInter

"""Unit tests for Sessions methods."""


def test_init():
    """test Sessions init"""
    sc = SessionsRandInter(autorun=True)
    assert len(sc.sessions) == cfg.n_sessions


def test_check_sess_attendees(config_event_defaults, get_random_seed):
    """test for check_sess_attendees"""
    sc = SessionsRandInter(get_random_seed)
    good_session = [x for x in range(cfg.n_attendees)]
    sc.build_sessions()
    # each session must include attendees
    for k, v in sc.sessions.items():
        attend_list = [e for i in v for e in i]
        attend_list.sort()
        assert attend_list == good_session


def test_build_sessions(config_event_defaults, get_random_seed):
    """ test build sessions"""
    sc = SessionsRandInter(get_random_seed)
    sc.build_sessions()
    assert len(sc.sessions) == cfg.n_sessions

def test_update_card_interactions(config_event_defaults, get_random_seed):
    """ test update of interactions """
    sess = [[1, 3, 10, 8], [0, 6, 9], [4, 5, 7, 2]]
    sc = SessionsRandInter(get_random_seed)
    sc.update_card_interactions(sess)
    assert sc.all_cards[0].card_interactions[6] == 1
    assert sc.all_cards[0].card_interactions[9] == 1
    assert sc.all_cards[1].card_interactions[1] == 0
    assert sc.all_cards[1].card_interactions[10] == 1
    assert sc.all_cards[1].card_interactions[6] == 0
