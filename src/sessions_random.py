import random
import copy
from src import config as cfg
from src.sessions_algo import SessionsAlgo
from src import sessions_util as su
import logging
log = logging.getLogger(__name__)

'''
    use variables from cfg
    Build session dictionary 0 thru x
    Populate session dictionary by randomly shuffling the attendees list
    the sessions dictionary contains the outbreak sessions

'''


class SessionsRandom(SessionsAlgo):
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
        su.set_seed(seed)

        # autorun the session
        if autorun:
            self.run()

    def create_a_session(self, ) -> list:
        """ create a single session from the attendees list"""
        # shuffle the list
        random.shuffle(self.rand_attendees)
        sess = []
        for i in range(0, cfg.n_attendees, self.group_size):
            sess.append(sorted(self.rand_attendees[i: i + self.group_size]))

        return sess

    def build_sessions(self,) -> dict:
        """build sessions
           - this is the driver called by parent class run method
        """
        for i in  self.sessions.keys():
            self.n_groups, self.group_size = su.set_n_groups(i)
            sess = self.create_a_session()
            self.sessions[i] = sess
        return self.sessions

