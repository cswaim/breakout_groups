#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_sessions_random.py
#
#  Copyright 2023 cswaim <cswaim@tpginc.net>

import pytest
import os
import sys
import logging

from src import config as cfg
import bg_algo_compare as bac

"""Unit tests for bg_algo_compare """

def test_set_config():
    """ test set config variables"""
    bac.set_config()
    assert bac.cfg.report_cards == False
    assert bac.cfg.report_interactions_matrix == False
    assert bac.cfg.sys_run_stats_csv == 'run_stats_compare.csv'
    assert bac.cfg.sys_run_stats_txt == 'run_stats_compare.txt'

def test_get_args(monkeypatch):
    """test geting args"""
    monkeypatch.setattr(sys, 'argv', ['test_bg_algo_compare.py','-lc', '6',])
    parser = bac.bg_parser.get_parser()
    parms = parser.parse_args()
    assert parms.loop_cnt == 6

def test_run(tmp_path, monkeypatch):
    """ test run with default data loop x times"""
    monkeypatch.setattr(sys, 'argv', ['test_bg_algo_compare.py','-lc', '3',])
    parser = bac.bg_parser.get_parser()
    parms = parser.parse_args()
    assert parms.loop_cnt == 3
