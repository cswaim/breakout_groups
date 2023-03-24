import random
import copy
from src import config as cfg

'''
    Build session dictionary 1 thru x (not 0 offset)
    Populate session dictionary by randomly shuffling the attendees list
    the sessions dictionary contains the outbreak sessions

'''


class Sessions():
    """ Use random to build sessions"""

    groups = []
    sessions = {}
    rand_attendees = []

    def __init__(self,):
        """init"""  
        self.sessions = {i:[] for i in range(1, cfg.sessions +1)}
        self.rand_attendees = copy.copy(cfg.attendees_list)

    def create_a_session(self, ) -> None:
        """ create a single session from the attendees list"""
        # shuffle the list 
        random.shuffle(self.rand_attendees)
        sess = []
        for i in range(0, cfg.attendees, cfg.group_size):
            sess.append(sorted(self.rand_attendees[i: i + cfg.group_size]))

        return sess

    def build_sessions(self) -> None:
        """build sessions"""
        for i in  self.sessions.keys():
            sess = self.create_a_session()
            self.sessions[i] = sess
