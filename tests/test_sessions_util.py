"""SHow the distribution of interactions in a Sessio.
"""
import pytest
from src import config as cfg
from src import sessions_util as su


def test_init_cards(config_event_defaults):
    """test build dict of cards"""
    all_cards = su.init_cards()
    assert len(all_cards) == len(cfg.all_cards)


def test_update_cards(config_event_defaults):
    """test updating of individual cards based on sessions"""
    all_cards = su.init_cards()
    all_cards = su.update_cards(all_cards)
    # counters do not guarantee order by key, need to sort to compare
    for i in range(len(all_cards)):
        assert all_cards[i].sess_labels == cfg.all_cards[i].sess_labels
        assert sorted(all_cards[i].card_interactions) ==  sorted(cfg.all_cards[i].card_interactions)



def test_build_all_card_interactions(config_event_defaults):
    """test building of all card interactions"""
    all_card_interactions = su.build_all_card_interactions()
    assert all_card_interactions == cfg.all_card_interactions