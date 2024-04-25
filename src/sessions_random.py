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
        for i in range(0, cfg.n_attendees, cfg.group_size):
            sess.append(sorted(self.rand_attendees[i: i + cfg.group_size]))

        sess = su.assign_extra_attendees(sess)

        return sess

    def build_sessions(self,) -> list:
        """build sessions"""
        for i in  self.sessions.keys():
            sess = self.create_a_session()
            self.sessions[i] = sess
        return self.sessions

