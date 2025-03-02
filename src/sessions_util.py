from collections import Counter
from collections import deque

from itertools import combinations
from math import floor
import random

from numpy import integer
from src import config as cfg
from src.card import Card
import logging

log = logging.getLogger(__name__)

""" This is a collection of utilities used in creating sessions

    import the module:
        from src import sessions_util as su
    then all functions:
        su.functionname()
    """

def get_algorithms():
    """ return a list of pairs (session modules, class) from list
        ac = ['m1','cm1','m2','cm2','m3','cm3']
        algo = [['m1','cm1'],['m2','cm2'],['m3','cm3']]
    """
    algo_vals = cfg.sys_algorithm_compare
    algo = [[algo_vals[i], algo_vals[i+1]] for i in range(0, len(algo_vals), 2)]

    return algo

def set_seed(seed=None):
    """Sets the random seed.

    Args:
        seed: The random seed.

    Returns:
        None.
    """

    random.seed(seed)

def init_sessions(n_sess: int=cfg.n_sessions) -> dict:
    """Initializes a dictionary of sessions.

    Args:
        n_sess: The number of sessions.

    Returns:
        A dictionary of sessions, where each session is a list of groups.
    """

    sessions = {i:[] for i in range(0, cfg.n_sessions)}
    return sessions

def init_cards(nc=cfg.n_attendees) -> list:
    """Initializes a list of cards.

    Args:
        nc: The number of cards.

    Returns:
        A list of cards.
    """

    all_cards = []
    for i in range(nc):
        all_cards.append(Card(i))
    return all_cards

def assign_extra_attendees(k: int, sess: list) -> list:
    """Using a set number of groups in a session, allocate 'extra' attendees
        to the groups defined by n_groups variables
        assume n_goups = 3
               n_attendee = 11
               n_size = 3

        [ [1,2,3], [4,5,6], [7,8,9], [10,11]]

        returns:
        [ [1,2,3,10], [4,5,6], [7,8,9,11]]

    Args:
        sess: A list of groups.

    Returns:
        A list of groups, where the number of groups has been set to n_groups.
    """
    # check for override
    ng, gs = set_n_groups(k)

    g_used = []
    if len(sess) > ng and len(sess[-1]) != gs:
        for x in sess[-1]:
            # gen number until not used
            while (g:= random.randrange(ng )) in g_used:
                # reset g_used if attendees still exist but all groups have been used
                if len(g_used) >= ng:
                    g_used = []
            g_used.append(g)
            sess[g].append(x)
        # remove last group
        sess.pop()
    return sess

def update_cards(all_cards) -> list:
    """Updates the individual card iteractions and labels.

    Args:
        all_cards: A list of cards.

    Returns:
        A list of cards, where the individual card iteractions and labels have been updated.
    """

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
                all_cards[c].update_group_labels(glabel)
    return all_cards

def build_all_card_interactions() -> dict:
    """Builds a dict of all the interactions from all cards.
       Interactions with self are set to zero;
       for item 1 counter value 1 = 0, for item counter value 2 = 0 etc.

    Returns:
        A dict of all the interactions from all cards.
    """

    all_card_interactions = {}
    for c in cfg.all_cards:
        all_card_interactions[c.id] = c.card_interactions
        # zero interactions with self
        all_card_interactions[c.id][c.id] = 0

    return all_card_interactions


def print_item(prt_item, heading=''):
    """Prints either a list or dictionary.

    Args:
        prt_item: The item to print.
        heading: The heading for the printed item.

    Returns:
        None.
    """

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

def groups_of_attendees_to_list(session=None) -> list:
    """Compress groups of attendees into a single list of attendees."""
    all_attendees = []
    for group in session:
        for attendee in group:
            all_attendees.append(attendee)
    return all_attendees

def set_n_groups(sess_id) -> int:
    """check the session group_size overide and set group_size"""
    if sess_id in cfg.session_ng_overrides:
        n_groups = cfg.session_ng_overrides[sess_id]
        group_size = floor(cfg.n_attendees / n_groups)
    else:
        n_groups = cfg.orig_n_groups
        group_size = floor(cfg.n_attendees / n_groups)
    return n_groups, group_size