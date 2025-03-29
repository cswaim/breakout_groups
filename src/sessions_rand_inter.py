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
            for i in range(0, cfg.n_attendees, self.group_size):
                sess.append(sorted(self.rand_attendees[i: i + self.group_size]))
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
            i_list = self.all_cards[c].card_interactions.most_common()

            # loop until group >= group_size
            while len(group) < self.group_size:
                # get min interaction for card that is not in used
                min_int = self.get_min_interaction(i_list)

                # break out of while if all attendees assigned
                if min_int is None:
                    break
                # get the next low interaction attendee if in used
                elif min_int in self.used_attendee or min_int == c:
                    pass
                else:
                    group.append(min_int)
                    self.used_attendee.add(min_int)

            # chk group size, append to session if group size
            if len(group) >= self.group_size:
                # add group to sess and reset
                sess.append(copy.copy(group))
                group.clear()

        # append remainder to session
        if len(group) != 0:
            sess.append(group)
        return sess

    def get_min_interaction(self, i_list):
        """ get next card with lowest interaction count that is
            not in the used_attendee list
        """
        min_int = next((item[0] for item in reversed(i_list) if item[0] not in self.used_attendee), None)
        return min_int


    def interactions_weighted_random2(self, sess: list) -> list:
        """ Build random session with groups of attendees,
            optimizing for unique interactions
            and minimizing duplicates.
        """
        # Reset tracking variables
        self.used_attendee = set()  # Change to set for O(1) lookup
        available_attendees = set(self.rand_attendees.copy())
        random.shuffle(self.rand_attendees)

        while available_attendees:
            group = []
            # Start with a random unused attendee
            if not available_attendees:
                break

            # Get first attendee for the group
            seed_attendee = next(iter(available_attendees))
            group.append(seed_attendee)
            available_attendees.remove(seed_attendee)
            self.used_attendee.add(seed_attendee)

            # Fill the group with attendees who have had
            #  minimal interactions with current group
            while len(group) < self.group_size and available_attendees:
                # Score each available attendee based on previous
                #  interactions with current group
                best_candidate = None
                lowest_interaction_score = float('inf')

                for candidate in available_attendees:
                    # Calculate interaction score (lower is better)
                    interaction_score = sum(
                        self.all_cards[candidate].card_interactions[member]
                        for member in group
                        if member in self.all_cards[candidate].card_interactions
                    )

                    if interaction_score < lowest_interaction_score:
                        lowest_interaction_score = interaction_score
                        best_candidate = candidate

                if best_candidate:
                    group.append(best_candidate)
                    available_attendees.remove(best_candidate)
                    self.used_attendee.add(best_candidate)
                else:
                    break  # No suitable candidates left

            # Add completed group to session
            if group:
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
