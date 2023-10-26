from collections import Counter

import datetime
from src import reports_util as rptu
import pytest

"""Unit tests for report utilities"""

def test_set_rpt_date(config_event_defaults, tmp_path):
    """test setting of report date"""
    rptu.set_rpt_date()
    assert True == isinstance(rptu.dt, datetime.datetime)
