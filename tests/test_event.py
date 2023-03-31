from src.event import Event

def test_find_missing_persons(get_config, get_random_seed):
    assert True

def test_get_interactions(event_cards):
    event = Event()
    result = event.get_interactions(all_cards=event_cards)
    assert result

def test_show_interactions_by_persons(event_cards):
    event = Event()
    result = event.show_interactions_by_persons(all_cards=event_cards)
    assert result is None
