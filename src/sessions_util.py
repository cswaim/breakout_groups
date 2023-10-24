from collections import Counter
from itertools import combinations
import random
from src import config as cfg
from src.card import Card
import logging

log = logging.getLogger(__name__)

"""Utilities for sessions

    This is a collection of utilities used in creating sessions

    import the module:
        from src import sessions_util as su
    then all functions:
        su.functionname()
"""

def get_algorithms():
    """ return a list of session modules, session algorithms"""
    algo = (
        ("sessions_random","SessionsRandom"),
        ("sessions_random_interactions","SessionsRandomInteractions"),
        ("sessions_comb","SessionsComb"),
    )

    return algo


def set_seed(seed=None):
    random.seed(seed)

def init_sessions(n_sess: int=cfg.n_sessions) -> dict:
    """build and initialize the sessions dict"""
    sessions = {i:[] for i in range(0, cfg.n_sessions)}
    return sessions

def init_cards(nc=cfg.n_attendees) -> list:
    """ build the all_cards dict"""
    all_cards = []
    for i in range(nc):
        all_cards.append(Card(i))
    return all_cards

def set_num_groups(sess: list) -> list:
    """set the number of goups in a session, randomly allocating members to other groups"""

    g_used = []
    if len(sess) > cfg.n_groups and len(sess[-1]) != cfg.group_size:
        for x in sess[-1]:
            # gen number until not used
            while (g:= random.randrange(cfg.n_groups )) in g_used:
                # reset g_used if attendees still exist but all groups have been used
                if len(g_used) >= cfg.n_groups:
                    g_used = []
            g_used.append(g)
            sess[g].append(x)
        # remove last group
        sess.pop()
    return sess

def update_cards(all_cards) -> list:
    """ update individual card iteractions and labels"""
    # k is session num,ber v is group list
    for k, v in cfg.sessions.items():
        # update card with group info, n grp num and g is group list of attendees
        for n, g in enumerate(v):
            upd_dict = all_cards[0].convert_grp_to_dict(g)
            for c in g:
                all_cards[c].update_cards(upd_dict)
                # set the group label, if label not found, use default
                try:
                    glabel = cfg.group_labels[k][n]
                except:
                    glabel = f"group{n}"
                all_cards[c].update_sess_labels(glabel)
    return all_cards

def build_all_card_interactions() -> dict:
    """build a list of all the interactions from all cards """
    all_card_interactions = {}
    for c in cfg.all_cards:
        all_card_interactions[c.id] = c.card_interactions

    return all_card_interactions

def print_item(prt_item, heading=''):
    """print either a list or dictionary"""
    prt_line = " {:02} - {}"

    print(f"--- {heading} ---")

    # if dict
    if isinstance(prt_item, dict):
        for i, val in prt_item.items():
            print(prt_line.format(i, val))
    # list or dict
    elif isinstance(prt_item, list) or isinstance(prt_item, tuple):
        for i, val in enumerate(prt_item):
            print(prt_line.format(i, val))
    else:
        print("**Error:  item is not a dict, list or tuple")