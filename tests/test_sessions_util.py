"""Tests for the distribution of interactions in a Session.
"""
import pytest

from src import config as cfg
from src.sessions_util import SessionsUtils as su


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


"""Happy day test the helper method"""
def test_make_sessions_returned():
    # breakpoint()
    sr = su.make_sessions_returned(n_attendees=12,
                                group_size=4,
                                n_sessions=5)
    assert sr.n_attendees == 12
    assert sr.group_size == 4
    assert sr.sessions == [[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]],
            [[11, 0, 1, 2], [3, 4, 5, 6], [7, 8, 9, 10]],
            [[10, 11, 0, 1], [2, 3, 4, 5], [6, 7, 8, 9]],
            [[9, 10, 11, 0], [1, 2, 3, 4], [5, 6, 7, 8]]]
    sr = su.make_sessions_returned(n_attendees=11,
                                group_size=4,
                                n_sessions=5)
    assert sr.n_attendees == 11
    assert sr.group_size == 4

"""Test for one orphan.
   WHen groups are formed, there is always one attendee left out."""
def test_for_one_orphan_attendee():
    n_attendees = 13
    group_size = 4
    n_sessions = 5
    sr = su.make_sessions_returned(n_attendees=n_attendees,
                            group_size=group_size,
                            n_sessions=n_sessions)

    for session in sr.sessions:
            for group in session:
                assert (len(group) == group_size) or (len(group) == group_size+1)


"""Test for two orphans"""
def test_for_two_orphan_attendees():
    n_attendees = 22
    group_size = 5
    n_sessions = 3
    sr = su.make_sessions_returned(n_attendees=n_attendees,
                            group_size=group_size,
                            n_sessions=n_sessions)
    # breakpoint()
    for session in sr.sessions:
            for group in session:
                assert (len(group) == group_size) or (len(group) == group_size+1)


""" Three orphans make an acceptable group.
    Expect a group size of 3 somehwere in the session."""
def test_for_four_orphan_attendees():
    n_attendees = 19
    group_size = 5
    n_sessions = 3
    sr = su.make_sessions_returned(n_attendees=n_attendees,
                            group_size=group_size,
                            n_sessions=n_sessions)
    # breakpoint()
    for session in sr.sessions:
        for group in session:
            assert (len(group) == group_size) or (len(group) == group_size-1)
