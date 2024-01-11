from collections import Counter

import datetime
from src import reports_util as rptu
import pytest

from src import config as cfg

"""Unit tests for report utilities"""

def test_set_rpt_date(config_event_defaults, tmp_path):
    """test setting of report date"""
    rptu.set_rpt_date()
    assert True == isinstance(rptu.dt, datetime.datetime)

def test_calc_event_stats(config_event_defaults):
    """ test calc of event stats"""
    # with n_attendees = 11
    es = rptu.calc_event_stats()
    assert es['max_group_size'] == 4
    assert es['max_group_size_occurence'] == 2
    assert es['max_idivi'] == 12
    assert es['pui'] == 55
    assert es['max_pui'] == 60
    assert es['puc'] == 165
    assert es['gc'] == 12

    cfg.n_attendees = 9
    es = rptu.calc_event_stats()
    assert es['max_group_size'] == 3
    assert es['max_group_size_occurence'] == 0
    assert es['max_pui'] == 36

    cfg.n_attendees = 10
    es = rptu.calc_event_stats()
    assert es['max_group_size'] == 4
    assert es['max_group_size_occurence'] == 1
    assert es['max_pui'] == 48

    cfg.n_attendees = 12
    es = rptu.calc_event_stats()
    assert es['max_group_size'] == 4
    assert es['max_group_size_occurence'] == 0
    assert cfg.group_size == 4
    assert es['max_pui'] == 72

