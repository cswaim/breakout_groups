import src.config as cfg
from src.event import Event

from collections import Counter
import pytest

def test_event(config_event_defaults, get_random_seed):
    event = Event(get_random_seed)
    assert event.all_card_interactions == {}
    assert len(event.all_cards) == cfg.n_attendees

def test_build_card_interactions(get_random_seed, get_config):
    config_values = get_config
    # Test results assume a certain configuration
    if (    (config_values['n_attendees'] != 30)  or \
            (config_values['group_size'] != 6)  or \
            (config_values['n_groups'] != 5)  or \
            (config_values['sessions'] != 5) \
        ):
        pytest.skip("For this configuration expected values are unknown")
    event = Event(seed=get_random_seed)
    event.update_cards()
    # breakpoint()
    res0 = Counter({0: 5, 19: 3, 3: 2, 22: 2, 20: 2, 25: 2, 18: 2, 6: 2, \
        7: 1, 13: 1, 26: 1, 21: 1, 1: 1, 27: 1, 15: 1, 12: 1, 17: 1, 29: 1})
    res1 = Counter({1: 5, 18: 3, 23: 2, 24: 2, 20: 2, 22: 2, \
        16: 1, 17: 1, 21: 1, 25: 1, 9: 1, 11: 1, 29: 1, 0: 1, 27: 1, 7: 1, 12: 1, 3: 1, 13: 1, 28: 1})
    assert res0 == event.all_cards[0].card_interactions
    assert res1 == event.all_cards[1].card_interactions

# def test_get_interactions(event_cards):
#     event = Event()
#     result = event.get_interactions(all_cards=event_cards)
#     assert result

def test_show_interactions_by_persons(event_cards, get_random_seed):
    event = Event(get_random_seed)
    event.run()
    result = event.show_interactions_by_persons()
    assert result is None
