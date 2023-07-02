import random
import copy
from collections import Counter
from src import config as cfg
import logging
log = logging.getLogger(__name__)

from src.card import Card

'''
    use variables from cfg
    Build session dictionary 0 thru x
    Populate session dictionary by randomly shuffling the attendees list
        and gouping by least interactions
    the sessions dictionary contains the outbreak sessions

'''

class SessionsRandomInteractions():
    """ Use random to build sessions"""

    def __init__(self, seed=None, autorun=False) -> None:
        """init"""
        self.groups = []
        self.sessions = {i:[] for i in range(0, cfg.n_sessions)}
        self.interactions = {}
        self.rand_attendees = copy.copy(cfg.attendees_list)
        self.seed = seed
        random.seed(seed)
        self.all_cards = {}
        for i in range(cfg.n_attendees):
            self.all_cards[i] = Card(i)
        self.used_attendee = []
        if autorun:
            self.run()

    def create_a_session(self, sess_num ) -> list:
        """ create a single session from the attendees list"""
        # shuffle the list
        random.shuffle(self.rand_attendees)
        sess = []
        # for first session, use random then use interaction weighted random
        if sess_num == 0:
            for i in range(0, cfg.n_attendees, cfg.group_size):
                sess.append(sorted(self.rand_attendees[i: i + cfg.group_size]))
        else:
            sess = self.interactions_weighted_random(sess)

        # if last group is not full size group, randomly allocate members to other groups
        g_used = []
        if len(sess) > cfg.n_groups and len(sess[-1]) != cfg.group_size:
            for x in sess[-1]:
                # gen number until not used
                while (g:= random.randrange(cfg.n_groups )) in g_used: pass
                g_used.append(g)
                sess[g].append(x)
            # remove last group
            sess.pop()
        return sess

    def get_unused_attendee(self, i):
        """get attend id"""
        c = self.rand_attendees[i]
        if c in self.used_attendee:
            c_set = set(self.rand_attendees) - set(self.used_attendee)
            c = c_set.pop()
        return c

    def interactions_weighted_random(self, sess: list) -> list:
        """ build random session with interactions """
        self.used_attendee = []
        group = []
        random.shuffle(self.rand_attendees)
        for i in range(len(self.rand_attendees)):
            if len(self.used_attendee) == len(self.rand_attendees):
                break
            # get the card number
            c = self.get_unused_attendee(i)

            # get min interaction for card
            i_list = self.all_cards[c].card_interactions.most_common()
            min_int = i_list[-1][0]

            if len(group) < cfg.group_size:
                group.append(c)
                self.used_attendee.append(c)
            if len(group) < cfg.group_size:
                if min_int in self.used_attendee or min_int == c:
                    pass
                else:
                    group.append(min_int)
                    self.used_attendee.append(min_int)
            if len(group) >= cfg.group_size:
                # add group to sess and reset
                sess.append(copy.copy(group))
                group.clear()

        if len(group) != 0:
            sess.append(group)
        return sess

    def update_card_interactions(self, sess: list):
        """ use sess to update interactions"""
        # update card with group info, n grp num and g is group list of attendees
        for g in sess:
            upd_dict = self.all_cards[0].convert_grp_to_dict(g)
            for c in g:
                self.all_cards[c].update_cards(upd_dict)

    def build_sessions(self,) -> list:
        """build sessions"""
        for i in  self.sessions.keys():
            sess = self.create_a_session(i)
            self.sessions[i] = sess
            # update card interaction with sess
            self.update_card_interactions(sess)
        return


    def run(self,) -> None:
        """create the sessions"""
        log.info("beg sessions_random_interactions")
        self.build_sessions()
        log.info("end sessions_random_interactions")

