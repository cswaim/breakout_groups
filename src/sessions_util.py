from collections import Counter
from collections import deque

from itertools import combinations
import random
from src import config as cfg
from src.card import Card
from src.sessions_returned import SessionsReturned
import logging

log = logging.getLogger(__name__)

        
class SessionsUtils():
    """ This is a collection of utilities used in creating sessions

        These functions are called statically :: note no self in the function definition

        import the module:
            from src.sessions_util import SessionsUtils as su
        then all functions:
            su.functionname()
        """


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

    def set_num_groups(sess: list) -> list:
        """Sets the number of groups in a session.

        Args:
            sess: A list of groups.

        Returns:
            A list of groups, where the number of groups has been set.
        """

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
                    all_cards[c].update_sess_labels(glabel)
        return all_cards

    def build_all_card_interactions():
        """Builds a list of all the interactions from all cards.

        Returns:
            A list of all the interactions from all cards.
        """

        all_card_interactions = {}
        for c in cfg.all_cards:
            all_card_interactions[c.id] = c.card_interactions

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

    def make_sessions_returned(n_attendees=None,
                                group_size=None,
                                n_sessions=None):
        """Creates all sessions for an event, based on the values in the parameters.

        At the retreats, it seems the group size is a limiting factor.
        On the other hand, the number of groups grows and shrinks based on the number 
        of attendees.
        If a test wants to stipulate the number of groups, then calculate the
        group_size based on the desired number of groups prior to calling this method.

        Args:
            n_attendees: The number of attendees.
            group_size: The number of attendees in each group.
            n_sessions: The number of sessions.

        Returns:
            A SessionsReturned object containing all of the sessions.
        """

        if not n_attendees:
            n_attendees = cfg.n_attendees
        attendees = list(range(0, n_attendees))

        if not group_size:
            group_size = cfg.group_size

        if not n_sessions:
            n_sessions = cfg.n_sessions

        base = attendees
        sessions = []

        # For some variety in the test cases, rotate the members by one to the next group.
        # For example,
        # [[0, 1, 2] , [3, 4, 5]]   becomes   [[5, 0, 1], [2, 3, 4]]
        # etc.
        for new_attendee_order in range(1, n_sessions):
            new_attendee_order_d = deque(base)
            new_attendee_order_d.rotate(1)
            new_attendee_order = list(new_attendee_order_d)
            session = [base[group:group+group_size]
                        for group in range(0, len(attendees), group_size)]
            sessions.append(session)
            base = new_attendee_order

        # The rules for orphans prevent a group formed with only
        # one or two attendees.  Need at least three.  A group with
        # less than three attendees is disbanded and the attendees added
        # to other groups.

        for session in sessions:
            for group in session:
                # Due to orphans, do we need to disband this group?
                if len(group) < 3:
                    # Find a new group for this orphan attendee
                    for index_orphan, orphan in enumerate(group):
                        session[index_orphan].append(orphan)
                        # group.remove(orphan)
                    # Cleanup by removing the group since no orphans remain
                    session.remove(group)

        sr = SessionsReturned()
        sr.group_size = group_size
        sr.n_attendees = n_attendees
        sr.sessions = sessions

        return sr

    def groups_of_attendees_to_list(session=None):
        """Compress groups of attendees into a single list of attendees."""
        all_attendees = []
        for group in session:
            for attendee in group:
                all_attendees.append(attendee)
        return all_attendees