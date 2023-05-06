import pytest
import os
from src import config as cfg
from src.card import Card

""" Central repository for Pytest fixtures for breakout groups."""

@pytest.fixture(scope='session')
def create_folders(tmp_path_factory):
    """this is a setup/teardown example"""
    # set_up: set paths
    base_dir = tmp_path_factory / "breakout_groups" 
    base_dir.mkdir()
    base_dir = tmp_path_factory / "breakout_groups" + os.sep + "data" 
    base_dir.mkdir()
    cfg.datadir = str(base_dir) + os.sep

    # yield, to let all tests within the scope 
    yield 

    # tear_down: remove test dir & files
    if os.path.exists(tmp_path_factory):
        for pth, dir, files in os.walk(tmp_path_factory):
            for d in dir:
                for fl in files:
                    os.remove(f"{tmp_path_factory}{os.sep}{d}{fl}")
            for fl in files:
                os.remove(f"{tmp_path_factory}{fl}")
        os.rmdir(tmp_path_factory)

@pytest.fixture
def get_config():
    """Parses the configuration file values and returns them in a dict"""
    config = cfg.read_config_file(cfg.config)
    config_values = {}
    config_values['n_attendees'] = config.getint('EVENT','n_attendees')
    config_values['group_size'] = config.getint('EVENT','group_size')
    config_values['n_groups'] = config.getint('EVENT','n_groups')
    config_values['n_sessions'] = config.getint('EVENT','n_sessions')     
    return config_values

@pytest.fixture
def config_EVENTs():
    """set cfg variables to EVENT values"""
    cfg.n_attendees = 11
    cfg.n_groups = 3
    cfg.group_size = 3
    cfg.n_sessions = 4
    cfg.gen_attendees_list()
    cfg.group_labels = []   
    cfg.group_labels.append(["group1","group2","group3","group4","group5"])
    cfg.group_labels.append(["blue","red","green","yellow","pink"])
    cfg.group_labels.append(["Portales","Santa Fe","Taos","Chama","Cuba"])
    cfg.group_labels.append(["Elbert","Massive","Harvard","Blanca","La Plata"])
    cfg.sys_group_algorithm = 'sessions_random'
    cfg.sys_group_algorithm_class = 'SessionsRandom'
    return cfg

@pytest.fixture
def get_random_seed():
    return 3331

@pytest.fixture
def event_cards(get_config, get_random_seed):
    config_values = get_config
    card_1 = Card()
    n_attendees = config_values["n_attendees"]
    n_groups = config_values['n_groups']
    grouping_algorithm = card_1.random_grouping_algorithm(
        n_groups=n_groups, seed=get_random_seed)
    
    return card_1.cards_for_event(
        n_attendees=n_attendees, 
        n_groups=n_groups,
        grouping_algorithm = grouping_algorithm)