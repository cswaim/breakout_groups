import datetime
from src import config as cfg
from src.reports import Reports
import pytest

"""Unit tests for run statistics"""

def test_verify_report_options(config_event_defaults):
    """test cfg has all report flags """
    rpt = Reports()
    assert True == hasattr(cfg, "report_interactions_matrix")
    assert True == hasattr(cfg, "report_run_stats")
    assert True == hasattr(cfg, "report_cards")
