"""Tests for the distribution of interactions in a Session.
"""
import pytest

from src import config as cfg
from src import sessions_util as su


def test_init_cards(config_event_defaults):
    """test build dict of cards"""
    all_cards = su.init_all_cards()
    assert len(all_cards) == len(cfg.all_cards)

def test_update_cards(config_event_defaults):
    """test updating of individual cards based on sessions"""
    all_cards = su.init_all_cards()
    all_cards = su.update_cards(all_cards)
    # counters do not guarantee order by key, need to sort to compare
    for i in range(len(all_cards)):
        assert all_cards[i].group_labels == cfg.all_cards[i].group_labels
        assert sorted(all_cards[i].card_interactions) ==  sorted(cfg.all_cards[i].card_interactions)

def test_build_all_card_interactions(config_event_defaults):
    """test building of all card interactions"""
    all_card_interactions = su.build_all_card_interactions()
    assert all_card_interactions == cfg.all_card_interactions

def test_get_algorithms(config_event_defaults):
    """test get algorithms which converts the string of algorithms
        to a list of lists [[module,class], [module,class]]
    """
    rsp = [["sessions_random","SessionsRandom"], ["sessions_random_interactions","SessionsRandomInteractions"]]
    algos = su.get_algorithms()
    assert algos == rsp

def test_set_n_groups(config_event_defaults):
    """test set n_groups which checks for a n_group override
        in cfg.session_ng_override and use it
    """
    # test no override
    rsp = cfg.n_groups
    ng, gs = su.set_n_groups(0)
    assert ng == rsp

    # test override of first session
    rsp = 6
    cfg.session_ng_overrides[0] = 6
    ng, gs = su.set_n_groups(0)
    assert ng == rsp

    # reset session_ng_overrides
    cfg.session_ng_overrides.pop(0)