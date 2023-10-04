from collections import Counter
from collections import deque

from itertools import combinations
import random
from src import config as cfg
from src.card import Card
from src.sessions_returned import SessionsReturned
import logging

log = logging.getLogger(__name__)

"""Utilities for sessions """


class SessionsUtils:
    """ This is a collection of utilities used in creating sessions

        These functions are called statically :: note no self in the function definition

        import the module:
            from src.sessions_util import SessionsUtils as su
        then all functions:
            su.functionname()
    """


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

    def build_all_card_interactions():
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

        """For many reasons, this is easier as a hlper method than as a fixture."""
    def make_sessions_returned(n_attendees=None,
                            group_size=None,
                            n_sessions=None):
        """Based on values in the parameters, create all sessions for an event.
            At the retreats, it seems the group size is a limiting factor.
            On the other hand, the number of groups grows and shrinks based 
            on the number of attendees.
            If a test wants to stipulate the number of groups, then calculate the
            group_size based on the desired number of groups prior to calling this method.
        """

    # Attendees are simply the list of attendees, starting at zero
        if not n_attendees:
            n_attendees = cfg.n_attendees
        attendees = list(range(0,n_attendees))

        # Group_size is the number of attendees in each group.  It is a maximimum 
        # for each group.

        # THe number of groups is calculated (using Python split) 
        # so that as many groups as possible are formed
        #  without creating any groups with more attendees than than the group_size.
        if not group_size:
            group_size = cfg.group_size

        # For some variety in the test cases, rotate the members by one to the next group.
        # For example, 
        # [[0, 1, 2] , [3, 4, 5]]   becomes   [[5, 0, 1], [2, 3, 4]]
        # etc.
        if not n_sessions:
            n_sessions = cfg.n_sessions
        base = attendees
        sessions = []

        for new_attendee_order in range(1,n_sessions):
            new_attendee_order_d = deque(base)
            new_attendee_order_d.rotate(1)
            new_attendee_order = list(new_attendee_order_d)
            session = [base[group:group+group_size]   
            for group in range(0,len(attendees), group_size)]
            sessions.append(session)
            base = new_attendee_order

        # The rules for orphans prevent a group formed with only
        # one or two attendees.  Need at least three.  A group with
        # less than three attendees is disbanded and the attendees added
        # to other groups.
        
        # for session in range(0, n_sessions):
        #     for group in session:
        #         # do we need to disband this group?
        #         if len(group) < 3:
        #             next_available_home = 0
                    


        sr = SessionsReturned()
        sr.group_size = group_size
        sr.n_attendees = n_attendees
        sr.sessions = sessions

        return sr