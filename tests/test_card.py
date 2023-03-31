from src.card import Card

from collections import Counter
import pytest

"""Unit tests for Card methods."""

def test_init():
    card = Card()
    assert card.name is None
    assert card.breakout_groups == []


def test_random_grouping_algorithm(get_random_seed):
    num = 0
    seed = get_random_seed
    groups = 5
    results = []
    card_1 = Card()
    num_gen = card_1.random_grouping_algorithm(n_groups=groups, seed=seed)
    while num < 30:
        num +=1
        results.append(next(num_gen))
    c = Counter(results)
    assert c[1] == 7
    assert c[2] == 4
    assert c[3] == 8
    assert c[4] == 6
    assert c[5] == 5


def test_cards_for_event(get_config, get_random_seed):
    card_1 = Card()
    config = get_config
    n_attendees = config.getint('DEFAULT','attendees')
    groups_per_session = config.getint('DEFAULT','groups_per_session')
    grouping_algorithm = card_1.random_grouping_algorithm(
        n_groups=groups_per_session, seed=get_random_seed)
    
    result = card_1.cards_for_event(
        n_attendees=n_attendees, 
        groups_per_session=groups_per_session,
        grouping_algorithm = grouping_algorithm)

    assert result
   

def test_print_the_cards_by_person(event_cards):
    card_1 = Card()
    result = card_1.print_the_cards_by_person(event_cards)
    assert result is None


def test_print_the_cards_by_session(event_cards):
    card_1 = Card()
    result = card_1.print_the_cards_by_session(event_cards)
    assert result is None