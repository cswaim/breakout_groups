from collections import Counter

import os
from src import config as cfg
from src import report_utils as rptu
import pytest

"""Unit tests for Interactions Matrix report."""

def test_cardpdf(config_event_defaults, tmp_path):
    """test cardpdf"""
    # base_dir = tmp_path / "breakout_groups"
    # base_dir.mkdir()
    # cfg.datadir = str(base_dir) + os.sep
    rptu.card_pdf()
    print('')
    result = []
    assert result[1][1] == 4

def test_print_card_header(config_event_defaults, tmp_path):
    """test printing of card header"""
    print('')
    result = rptu.print_card_header(cfg.event_title, cfg.event_subtitle, cfg.event_date)
    assert result == None

