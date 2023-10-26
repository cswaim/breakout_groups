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
        attend_list = [e for i in v.sessions for e in i]
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


def test_init_from_cfg_and_algorithm(get_random_seed):
    """Test for the method:  SessionsVerticalIntersection.__init__.
    Any changes (additions, modifications, or deletes) to instance variables should FAIL.

    Here we test that the instance variables in SessionsVerticalIntersection are
    exactly as expected by this test.  This test type is "all and only".

    If you wish to experiment with different values for configuration variables, or for
    instance variables, consider making changes to the values in fixtures.  The principle
    is that tests manipulate input values, not by changes to config files or source.
    """

    # Create the default object.  Check the expected value of each instance variable. 
    svi = SessionsVerticalIntersection(seed=get_random_seed, autorun=False)
    assert svi.groups ==[]
    assert svi.sessions == {i:[] for i in range(0, cfg.n_sessions)}
    assert svi.interactions == {}
    assert svi.rand_attendees == cfg.attendees_list.copy()
    assert svi.seed == get_random_seed

    # Has the number of instance variables increased or decreased?
    assert len( vars(svi) ) == 7


def test_integration_one(get_random_seed):
    """
    A crude, high level, integration test.

    ToDo: Probably should also unit test each of the methods used here.
    """
    svi = SessionsVerticalIntersection(seed=get_random_seed, autorun=False)
    svi_out = svi.build_sessions()
    assert type(svi_out)  == dict
    


def test_make_svi_fixture(make_svi):
    """
    A test of the factory fixture named "make_svi".

    Was an instance of the algorithm class created successfully?
    """
    svi = make_svi(expected_yield=2)
    svi_returned = svi.build_sessions()
    assert type(svi_returned)  == dict
    assert svi.expected_yield ==2


def test_printing_turned_off(make_svi):
    """
    Can printing be turned on and off?

    For now, manually observe that printing is off.
    N.B. To see printing or not, run the tests with the -s parameter, for example:

    % cd tests
    % pytest test_sessions_vertical_intersection.py -s 

    or for a single test

    $ pytest test_sessions_vertical_intersection.py -s -k test_printing_turned_off

    An automated approach will require capturing and analyzing sys.stdout
    """
    svi = make_svi(printing=False)
    svi_returned = svi.build_sessions()
    # For now, just manually observe that nothing was printed.
    assert type(svi_returned)  == dict
    

@pytest.mark.parametrize("a_yield", [1,2,3,4,5,6,7])
def test_many_expected_yields(make_svi, a_yield):
    """
    Example of many runs with different values for expected_yield.

    Each value in the list above is used in a separate run.  Hence, this test
    will be run many times.
    """
    svi = make_svi(expected_yield=a_yield)
    svi_returned = svi.build_sessions()
    assert type(svi_returned)  == dict
    assert svi.expected_yield == a_yield
