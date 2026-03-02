from src import config as cfg
from src.event import Event
from src import sessions_util as su


def test_run_a_event(config_event_defaults, get_random_seed):
    """integration test for full event run"""
    event = Event(seed=get_random_seed)
    event.run()

    assert len(event.sessions) == cfg.n_sessions
    assert len(event.all_cards) == cfg.n_attendees
    assert len(event.all_card_interactions) == cfg.n_attendees
    assert cfg.sessions == event.sessions
    assert cfg.all_cards == event.all_cards
    assert cfg.all_card_interactions == event.all_card_interactions

    for sess_num, groups in event.sessions.items():
        all_attendees = su.groups_of_attendees_to_list(groups)
        assert len(all_attendees) == cfg.n_attendees
        assert len(set(all_attendees)) == cfg.n_attendees

    for card_id, interactions in event.all_card_interactions.items():
        assert interactions[card_id] == 0
