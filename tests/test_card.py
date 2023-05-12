from src.card import Card

from collections import Counter
import pytest

"""Unit tests for Card methods."""

def test_init():
    card = Card(1)
    assert card.name is None
    assert card.id == 1


# def test_random_grouping_algorithm(get_random_seed):
#     num = 0
#     seed = get_random_seed
#     groups = 5
#     results = []
#     card_1 = Card(1)
#     num_gen = card_1.random_grouping_algorithm(n_groups=groups, seed=seed)
#     while num < 30:
#         num +=1
#         results.append(next(num_gen))
#     c = Counter(results)
#     assert c[1] == 7
#     assert c[2] == 4
#     assert c[3] == 8
#     assert c[4] == 6
#     assert c[5] == 5


# def test_cards_for_event(get_config, get_random_seed):
#     card_1 = Card(1)
#     config_values = get_config
#     n_attendees = config_values["n_attendees"]
#     n_groups = config_values['n_groups']
#     grouping_algorithm = {0:[[1, 6, 8], [0, 3, 5, 4], [2, 7, 9]],
#                           1:[[0, 5, 6, 8], [1, 2, 7], [3, 4, 9]],
#                           2:[[1, 4, 7, 3], [2, 6, 8], [0, 5, 9]],
#                           3:[[3, 5, 9, 4], [1, 6, 8], [0, 2, 7]],
#                         }
    
#     result = card_1.cards_for_event(
#         n_attendees=n_attendees, 
#         n_groups=n_groups,
#         grouping_algorithm=grouping_algorithm)

#     assert result
   

def test_print_the_cards_by_person(config_event_defaults, event_cards):
    cfg = config_event_defaults
    card_1 = Card(1)
    print('')
    result = card_1.print_the_cards_by_person(event_cards)
    assert result == cfg.n_attendees


def test_print_the_cards_by_session(event_cards):
    card_1 = Card(1)
    result = card_1.print_the_cards_by_session(event_cards)
    assert result is None