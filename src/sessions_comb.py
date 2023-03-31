import itertools as it
from itertools import combinations
from itertools import chain
import random
import math
import copy
import functools as ft
from src import config as cfg

'''
The group_items function takes three arguments:

    items: The list of items to be grouped into subsets.
    subset_size: The size of each subset.
    num_rounds: The number of rounds to be conducted.

The function returns a list of lists, where each inner list represents a subset of items for each round.

The function first creates the subsets randomly for the first round, and then uses the algorithm I described earlier to create subsets for subsequent rounds. The function keeps track of which subsets each item has been assigned to in previous rounds to ensure that no item is assigned to the same subset again.

Note that the code assumes that the number of items is a multiple of the subset size, so if the last subset is not full, it will be dropped. If this is a problem, you can modify the code to handle the remaining items in some way (e.g., by adding them to the previous subset).

'''

class Sessions():
    """ Use combinations to build sessions"""

    groups = []
    sessions = {}
    used_groups = []
    session_attendees = []

    def __init__(self,):
        """init"""  
        self.sessions = {i:[] for i in range(1, cfg.n_sessions +1)}

    def gen_combinations(self, attendee_list, group_size) -> None:
        """ gen all possible combinations of group_size"""
        gc = list(it.combinations(attendee_list, group_size))
        
        # gc = [list(g) for g in gc]
        newgc =[]
        for g in gc:
            gs = sorted(g)
            newgc.append(gs)

        self.groups = newgc
        return 

    def groups_to_sessions(self,) -> None:
        """ create session which contains groups_per_session with each attendee in each session"""

        # mix up the groups
        random.shuffle(self.groups)

        # build session dict     
        self.sessions = {i:[] for i in range(1, cfg.n_sessions +1)}
        self.build_first_session()

        gcnt = 0
        # loop until out of groups or all sessions built
        while (sess_cnt := len([b[0] for b in self.sessions.values() if b])) < cfg.n_sessions and gcnt < len(self.groups):
            print(f"inloop {len(self.groups)} - {gcnt}", end="\r")
            # get non empty session count
            sess_cnt += 1

            self.session_attendees = []
            # loop until all attendees are assigned in session
            while self.session_attendees != cfg.attendees_list:
                sess = self.build_a_session()
                sess_complete = self.evaluate_sess(sess)

            if sess_complete:
                self.add_to_sessions(sess_cnt, sess)
                self.update_used_groups()
        
            gcnt += 1
        print()

        return 

    def build_first_session(self, ) -> list:
        """ build first session"""
        # shuffle the list for the first build
        rand_atnd = copy.copy(cfg.attendees_list)
        # random.shuffle(rand_attd)

        sess = []
        for i in range(0, cfg.n_attendees, cfg.group_size):
            sess.append(sorted(rand_atnd[i: i + cfg.group_size]))
       
        self.add_to_sessions(1, sess)
        self.update_used_groups()

        return 

    def add_to_sessions(self, inx, sess) -> None:
        """add session groups to sessions list """
        self.sessions[inx] = sess
        for g in self.sessions[inx]:
            self.used_groups.append(g)

    def update_used_groups(self,) -> None:
        """ check the groups and remove any used groups"""
        for k,v in enumerate(self.groups):
            if v in self.used_groups:
                del self.groups[k]

    def build_a_session(self,) -> list:
        """build a seesion from unused groups"""
        sess = []

        # for each session loop through groups and build a session
        sess.append(self.groups[0])
        for i in range(cfg.n_groups):
            # loop thru groups,
            for j, g in enumerate(self.groups):
                if sess[i] == self.groups[j]:
                    pass
                else:
                    # check for dup attendees
                    temp_g = [a for a in self.groups[j] if a not in chain.from_iterable(sess)]
                    if len(temp_g) == len(g):
                        # it is a good group for session
                        sess.append(g)
                        break
        return sess

    def evaluate_sess(self, sess) -> None:
        """evaluate groups, build session and ensure all attendees have been assigned"""

        # final check to make sure all attendees have been assigned
        sess_complete = self.check_sess_attendees(sess)
        if sess_complete:
            pass
        else:
            # reset 
            pass
        return sess_complete

    def check_sess_attendees(self, sess) -> bool:
        """make sure all attendees have been assigned to a session"""
        sess_attendees = []
        for g in sess:
            for a in g:
                sess_attendees.append(a)
        sess_attendees.sort()

        self.session_attendees = sess_attendees 
        res = sess_attendees == cfg.attendees_list
        return res

    def build_sessions(self) -> None:
        """build sessions"""
        self.gen_combinations(cfg.attendees_list, cfg.group_size)
        print(f"     comb: {len(self.groups)}")
        # print(f"math.comb: {math.comb(len(cfg.attendees_list), cfg.group_size)}")

        # for g in groups:
        #     calc_group_similarity(g)
        self.groups_to_sessions()
        # print(f"{len(self.sessions)}: {self.sessions}")