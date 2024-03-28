import src.config as cfg
from src.event import Event

from collections import Counter
import pytest

def test_event(config_event_defaults, get_random_seed):
    """test setup of an event"""
    event = Event(get_random_seed)
    assert event.all_card_interactions == {}
    assert len(event.all_cards) == cfg.n_attendees

def test_build_card_interactions(get_random_seed, config_event_defaults):
    """ test build tnteractions """
    event = Event(seed=get_random_seed)
    event.update_cards()
    res0 = Counter({0:0, 1:1, 3:2, 5:2, 6:2, 7:1, 9:2})
    res1 = Counter({0:1, 1:0, 2:2, 3:1, 4:1, 5:1, 7:3, 9:1})
    assert res0 == event.all_cards[0].card_interactions
    assert res1 == event.all_cards[1].card_interactions

    # verify interactions are within range
    # group_size - 1 eliminates self interactions
    i_min = (cfg.group_size -1) * cfg.n_sessions
    max_grp_size = 0
    for k, v in cfg.sessions.items():
        mgs = len(max(v, key=len))
        if mgs > max_grp_size:
            max_grp_size = mgs
    i_max = (max_grp_size - 1) * cfg.n_sessions
    interaction_limit_errors = []
    for k, v in cfg.all_card_interactions.items():
        n_interact = v.total()
        if i_min <= n_interact <= i_max:
            continue
        else:
            interaction_limit_errors.append(f"interaction {k} : {n_interact} is < {i_min} or > {i_max}")
    if interaction_limit_errors:
        for err in interaction_limit_errors:
            print(err)
    assert [] == interaction_limit_errors


# def test_get_interactions(event_cards):
#     event = Event()
#     result = event.get_interactions(all_cards=event_cards)
#     assert result

def test_show_interactions_by_persons(event_cards, get_random_seed):
    event = Event(get_random_seed)
    event.run()
    result = event.show_interactions_by_persons()
    assert result is None
