from collections import Counter

import os
from src import config as cfg
from src import report_utils as rptu
import pytest

"""Unit tests for report utilities"""

def test_print_card_header(config_event_defaults, tmp_path):
    """test printing of card header"""
    print('')
    result = rptu.print_card_header(cfg.event_title, cfg.event_subtitle, cfg.event_date)
    assert result == None

