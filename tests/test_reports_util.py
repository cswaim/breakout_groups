from collections import Counter

import datetime
from src import reports_util as rptu
import pytest

"""Unit tests for report utilities"""

def test_set_rpt_date(config_event_defaults, tmp_path):
    """test setting of report date"""
    rptu.set_rpt_date()
    assert True == isinstance(rptu.dt, datetime.datetime)

def test_calc_event_stats(config_event_defaults):
    """ test calc of event stats"""
    es = rptu.calc_event_stats()
    assert es['max_group_size'] == 4
    assert es['max_group_sise_occurence'] == 2
    assert es['max_idivi'] == 12
    assert es['pui'] == 55
    assert es['max_pui'] == 32
    assert es['puc'] == 165
    assert es['gc'] == 12
