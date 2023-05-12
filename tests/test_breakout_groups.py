#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_sessions_random.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>
 
import pytest
import os
import logging

from src import config as cfg
from breakout_groups import BreakoutGroups

"""Unit tests for Sessions methods."""


def test_init():
    """test Sessions init"""
    bg = BreakoutGroups()
    assert bg.n_sessions == cfg.n_sessions
    assert bg.n_attendees == cfg.n_attendees


def test_print_variables(config_event_defaults):
    """test of print of event info"""
    bg = BreakoutGroups()
    bg.print_variables()
    assert(True == True)


def test_run(tmp_path, config_event_defaults, get_random_seed):
    """ test run with default data"""
    base_dir = tmp_path / "breakout_groups" 
    base_dir.mkdir()
    cfg.datadir = str(base_dir) + os.sep
    bg = BreakoutGroups(get_random_seed)
    bg.run()
    assert len(bg.event.sess.sessions) == cfg.n_sessions 
