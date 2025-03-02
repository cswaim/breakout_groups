import random
import copy
from collections import Counter
from src import config as cfg
from src.sessions_algo import SessionsAlgo
import logging
log = logging.getLogger(__name__)

from src.card import Card
from src import sessions_util as su

'''
    Populate session dictionary by randomly shuffling the attendees list
        and gouping by least number of interactions

'''

class SessionsRandInter(SessionsAlgo):
    """ Use random to build sessions"""

    def __init__(self, seed=None, autorun=False) -> None:
        """init"""
        super().__init__(seed, autorun)

        # allow n_groups to be overridden by session
        self.n_groups = cfg.n_groups
        self.group_size = cfg.group_size

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

        # autorun the session
        if autorun:
            self.run()

    def create_a_session(self, sess_num ) -> list:
        """ create a single session from the attendees list"""
        # shuffle the list
        random.shuffle(self.rand_attendees)
        sess = []
        # for first session, use random then use interaction weighted random
        if sess_num == 0:
            for i in range(0, cfg.n_attendees, self.group_size):
                sess.append(sorted(self.rand_attendees[i: i + self.group_size]))
        else:
            sess = self.interactions_weighted_random(sess)

        # if last group is not full size group, randomly allocate members to other groups
        #sess = su.assign_extra_attendees(sess)

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

            if len(group) < self.group_size:
                group.append(c)
                self.used_attendee.append(c)

                if min_int in self.used_attendee or min_int == c:
                    pass
                else:
                    group.append(min_int)
                    self.used_attendee.append(min_int)
            if len(group) >= self.group_size:
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

    def build_sessions(self,) -> dict:
        """build sessions
           - this is the driver called by parent class run method
        """
        for i in  self.sessions.keys():
            self.n_groups, self.group_size = su.set_n_groups(i)
            sess = self.create_a_session(i)
            self.sessions[i] = sess
            # update card interaction with sess
            self.update_card_interactions(sess)
        return self.sessions
