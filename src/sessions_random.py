import random
import copy
from src import config as cfg

'''
    Build session dictionary 1 thru x (not 0 offset)
    Populate session dictionary by randomly shuffling the attendees list
    the sessions dictionary contains the outbreak sessions

'''


class SessionsRandom():
    """ Use random to build sessions"""

    def __init__(self, autorun=True):
        """init"""  
        self.groups = []
        self.sessions = {i:[] for i in range(0, cfg.n_sessions)}
        self.interactions = {}
        self.rand_attendees = copy.copy(cfg.attendees_list)
        if autorun:
            self.run()

    def create_a_session(self, ) -> list:
        """ create a single session from the attendees list"""
        # shuffle the list 
        random.shuffle(self.rand_attendees)
        sess = []
        for i in range(0, cfg.n_attendees, cfg.group_size):
            sess.append(sorted(self.rand_attendees[i: i + cfg.group_size]))
        
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

    def build_sessions(self, seed=None) -> list:
        """build sessions"""
        random.seed(seed)
        for i in  self.sessions.keys():
            sess = self.create_a_session()
            self.sessions[i] = sess
        return self.sessions


    def run(self,) -> list:
        """create the sessions"""
        self.sessions = self.build_sessions()
    