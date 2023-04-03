from collections import Counter
import src.config as cfg
from src.event import Event

def test_find_missing_persons(config_defaults, get_random_seed):
    assert True

def test_build_cards(config_defaults):
    """test build of cards (11 attendees/cards)"""
    event = Event()
    res = 11
    assert res == len(event.cards)

def test_build_cards(config_defaults, get_random_seed):
    """test build of cards (11 attendees/cards)"""
    event = Event(seed=get_random_seed)
    event.update_card_interactions()
    res0 = Counter({0:4, 5:2, 6:2, 3:2, 9:2, 1:1, 7:1})
    res1 = Counter({1:4, 7:3, 9:1, 3:1, 4:1, 5:1, 2:2, 0:1})
    assert res0 == event.cards[0].card_interactions
    assert res1 == event.cards[1].card_interactions

def test_all_card_interactions(config_defaults, get_random_seed):
    """test build of all_card_interactions list"""
    event = Event(seed=get_random_seed)
    event.update_card_interactions()
    event.build_all_card_interactions()
    res0 = Counter({0:4, 5:2, 6:2, 3:2, 9:2, 1:1, 7:1})
    res1 = Counter({1:4, 7:3, 9:1, 3:1, 4:1, 5:1, 2:2, 0:1})
    assert res0 == event.all_card_interactions[0]
    assert res1 == event.all_card_interactions[1]


# def test_get_interactions(event_cards):
#     event = Event()
#     result = event.get_interactions(all_cards=event_cards)
#     assert result

# def test_show_interactions_by_persons(event_cards):
#     event = Event()
#     result = event.show_interactions_by_persons(all_cards=event_cards)
#     assert result is None
