import pytest
from src import config as cfg
from src.card import Card

""" Central repository for Pytest fixtures for breakout groups."""

@pytest.fixture
def get_config():
    config = cfg.read_config_file(cfg.config)
    # assert config.getint('DEFAULT','attendees') == 30
    # assert config.getint('DEFAULT','group_size') == 6
    # assert config.getint('DEFAULT','groups_per_session') == 5
    # assert config.getint('DEFAULT','sessions') == 3     
    return config

@pytest.fixture
def get_random_seed():
    return 3331

@pytest.fixture
def event_cards(get_config, get_random_seed):
    card_1 = Card()
    config = get_config
    n_attendees = config.getint('DEFAULT','attendees')
    groups_per_session = config.getint('DEFAULT','groups_per_session')
    grouping_algorithm = card_1.random_grouping_algorithm(
        n_groups=groups_per_session, seed=get_random_seed)
    
    return card_1.cards_for_event(
        n_attendees=n_attendees, 
        groups_per_session=groups_per_session,
        grouping_algorithm = grouping_algorithm)