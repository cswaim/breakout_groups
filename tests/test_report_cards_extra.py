from collections import Counter

import os
from src import config as cfg
from src.reports_cards_extra import ReportsCardsExtra
import pytest

"""Unit tests for exta cards processing."""

def test_card_init(config_event_defaults, tmp_path):
    """test card init"""
    rce = ReportsCardsExtra()
    assert len(rce.extra_cards) == cfg.n_extra_cards

def test_update_extra_cards_labels(config_event_defaults, tmp_path):
    """test card print to console"""
    rce = ReportsCardsExtra()
    rce.add_extra_cards_to_group()
    rce.update_extra_cards_labels()

    assert rce.extra_cards[0].group_labels[0] == "group2"
    assert rce.extra_cards[0].group_labels[1] == "blue"
    assert rce.extra_cards[0].group_labels[2] == "Santa Fe"
    assert rce.extra_cards[0].group_labels[3] == "Massive"
    assert rce.extra_cards[1].group_labels[0] == "group1"
    assert rce.extra_cards[1].group_labels[1] == "blue"
    assert rce.extra_cards[1].group_labels[2] == "Portales"
    assert rce.extra_cards[1].group_labels[3] == "Elbert"

def test_update_sess_group(config_event_defaults, create_folders):
    """test card output to text file"""
    rce = ReportsCardsExtra()
    rce.update_sess_group(0, 2, 1)

    assert rce.sessions[2][1] == [1, 2, 7, 11]
    assert rce.extra_sess[2][1] == [11]

def test_add_extra_cards_to_group(config_event_defaults, create_folders):
    """test add card to group"""
    rce = ReportsCardsExtra()
    rce.add_extra_cards_to_group()
    print(rce.sessions)
    print(rce.extra_sess)

    assert rce.sessions[0][1] == [0, 5, 6, 11]
    assert rce.sessions[1][0] == [7, 8, 10, 11, 12]
    assert rce.sessions[2][1] == [1, 2, 7, 11]
    assert rce.sessions[3][1] == [0, 1, 7, 11]
    assert rce.extra_sess[0][1] == [11]
    assert rce.extra_sess[1][0] == [11, 12]
    assert rce.extra_sess[2][1] == [11]
    assert rce.extra_sess[3][1] == [11]
