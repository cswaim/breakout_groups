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
        self.sessions = su.init_sessions(cfg.n_sessions)
        self.interactions = {}
        self.rand_attendees = copy.copy(cfg.attendees_list)
        self.seed = seed
        random.seed(seed)
        self.all_cards = su.init_all_cards(cfg.n_attendees)
        self.used_attendee = set()

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
            # Build exactly n_groups base groups of group_size.
            for i in range(self.n_groups):
                beg = i * self.group_size
                end = beg + self.group_size
                sess.append(sorted(self.rand_attendees[beg:end]))

            # Assign any remaining attendees to existing groups using interaction scoring.
            overflow = self.rand_attendees[self.n_groups * self.group_size:]
            if len(overflow) != 0:
                sess = self.assign_overflow_with_interactions(sess, overflow)
        else:
            sess = self.interactions_weighted_random(sess)

        return sess

    def get_unused_attendee(self, i):
        """get attend id"""
        c = self.rand_attendees[i]
        if c in self.used_attendee:
            c_set = set(self.rand_attendees) - self.used_attendee
            c = c_set.pop()
        return c

    def interactions_weighted_random(self, sess: list) -> list:
        """ build random session with interactions """
        self.used_attendee = set()
        overflow = []
        group = []
        random.shuffle(self.rand_attendees)
        for i in range(len(self.rand_attendees)):
            if len(self.used_attendee) == len(self.rand_attendees):
                break
            # get the card number
            c = self.get_unused_attendee(i)
            group.append(c)
            self.used_attendee.add(c)

            # build a list of interactions for card/attendee
            # i_list = self.all_cards[c].card_interactions.most_common()

            # loop until group >= group_size
            while len(group) < self.group_size:
                # get min interaction for card that is not in used
                min_int = self.get_min_interaction(group)

                # break out of while if all attendees assigned
                if min_int is None:
                    break
                # # get the next low interaction attendee if in used
                # elif min_int in self.used_attendee or min_int == c:
                #     pass
                else:
                    group.append(min_int)
                    self.used_attendee.add(min_int)

            # chk group size, append to session if group size
            if len(group) >= self.group_size:
                # Keep exactly n_groups groups. Extra full groups become overflow.
                if len(sess) < self.n_groups:
                    sess.append(copy.copy(group))
                else:
                    overflow.extend(group)
                group.clear()

        # any remainder attendee(s) are overflow
        if len(group) != 0:
            overflow.extend(group)

        # assign overflow attendees into existing groups using interaction scoring
        if len(overflow) != 0:
            sess = self.assign_overflow_with_interactions(sess, overflow)

        return sess

    def get_group_interaction_score(self, attendee, group):
        """Return total prior interactions attendee has with a candidate group."""
        return sum(self.all_cards[attendee].card_interactions[g] for g in group)

    def assign_overflow_with_interactions(self, sess: list, overflow: list) -> list:
        """Assign overflow attendees to existing groups using minimum interaction cost.

        To spread attendees, groups are not reused until all groups are used once,
        then the cycle restarts.
        """
        if len(sess) == 0 or len(overflow) == 0:
            return sess

        g_used = []
        for attendee in overflow:
            available = [gi for gi in range(len(sess)) if gi not in g_used]
            if len(available) == 0:
                g_used = []
                available = list(range(len(sess)))

            scores = [(gi, self.get_group_interaction_score(attendee, sess[gi])) for gi in available]
            min_score = min(score for _, score in scores)
            candidate_groups = [gi for gi, score in scores if score == min_score]

            pick_group = random.choice(candidate_groups)
            sess[pick_group].append(attendee)
            g_used.append(pick_group)

        return sess

    def get_min_interaction(self, group):
        """ get next card with lowest interaction count that is
            not in the used_attendee list
        """
        # build a list of interactions for card/attendee
        lc = Counter({i: 0 for i in range(cfg.n_attendees)})
        for c in group:
            lc.update(self.all_cards[c].card_interactions)
        i_list = lc.most_common()[::-1]
        while True:
            min_int = next((item[0] for item in i_list if item[0] not in self.used_attendee), None)

            if min_int is None or min_int not in self.used_attendee:
                break
        return min_int

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
