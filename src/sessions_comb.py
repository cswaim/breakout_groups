import random
import itertools as it
from itertools import chain
import copy
from src import config as cfg
from src import sessions_util as su
import logging
log = logging.getLogger(__name__)

'''
    use variables from cfg
    Build session dictionary 0 thru x
    Generate possible combinations
    Populate session dictionary from the combinations
    the sessions dictionary contains the break out sessions

'''


class SessionsComb():
    """ Use combinations to build sessions"""

    def __init__(self, seed=None, autorun=False) -> None:
        """init"""
        self.groups = []
        self.interactions = {}
        self.seed = seed
        random.seed(seed)
        self.max_loop = 3
        self.sess_setup()
        if autorun:
            self.run()

    def sess_setup(self,):
        """ set up the datasets needed for create run"""
        self.random_attendees = copy.copy(cfg.attendees_list)
        self.sessions = {i:[] for i in range(0, cfg.n_sessions)}
        self.sess_attendees = {i:copy.copy(cfg.attendees_list) for i in range(0, cfg.n_sessions)}
        self.comb_dict = {i:[] for i in range(0, cfg.n_attendees)}
        self.comb_attendees = {i:copy.copy(cfg.attendees_list) for i in range(0, cfg.n_attendees)}

    def gen_group_combinations(self, ) -> None:
        """ create a dict of unique group combinations"""

        for sn in range(cfg.n_attendees):
            wl = copy.copy(self.comb_attendees[sn])
            if sn > 0:
                for d in range(sn):
                    if len(wl) > 0:
                        wl.pop(0)
            if len(wl) > 0:
                x = wl.pop(0)    # get first value
            while len(wl) > 0:
                if len(wl) < cfg.group_size:
                    break
                g = [x]
                for e in range(0, cfg.group_size - 1):
                    g.append(wl[e])
                self.comb_dict[sn].append(g)
                for e in range(0, cfg.group_size - 1):
                    wl.pop(0)
        # remove empty rows
        self.comb_dict = {k: v for k, v in self.comb_dict.items() if v}


        su.print_item(self.comb_dict, "comb dict")


    def create_sessions(self,):
        """ reformat the combinations and build the sessions"""
        self.build_first_group()

        # update session attendees
        for s, grp in self.sessions.items():
            for g in grp:
                self.update_sess_attendees(s, g)
        log.info("create_sessions:\n",self.sessions)

        # fill in session
        for s, g in self.sessions.items():
            # used to break out of while
            self.loop_cnt = 1
            while len(g) < cfg.n_groups and self.loop_cnt < self.max_loop:
                self.build_missing_groups(s, g)

        su.print_item(self.comb_dict, "comb dict after fill")
        # get missing attendees
        for s, a in self.sess_attendees.items():
            self.append_missed_attendees(s, a)

        # if last group is not full size group, randomly allocate members to other groups
        for s, g in self.sessions.items():
            g_used = []
            if len(g) > cfg.n_groups and len(g[-1]) != cfg.group_size:
                for x in g[-1]:
                    # gen group number until not used
                    while (gn:= random.randrange(cfg.n_groups )) in g_used: pass
                    g_used.append(gn)
                    g[gn].append(x)
                # remove last group
                g.pop()

    def update_sess_attendees(self, sess_num, group):
        """ remove attendee from sess_attendee list as they are placed in group"""
        for e in group:
            if e in self.sess_attendees[sess_num]:
                self.sess_attendees[sess_num].remove(e)

    def build_first_group(self):
        """rotate combinations and build the first group for each session """
        # rotate comb and build first group in each session
        if len(self.comb_dict[0]) >= cfg.n_sessions:
            wk_comb = copy.copy(self.comb_dict[0][0:cfg.n_sessions])
            add_groups = 0
        else:
            wk_comb = copy.copy(self.comb_dict[0])
            add_groups = cfg.n_sessions - len(self.comb_dict[0])
            for n in range(add_groups):
                wk_comb.append(self.comb_dict[1][n])
        for s, g in self.sessions.items():
            g.append(wk_comb[s])

        # delete the allocated groups
        for x in range(cfg.n_sessions):
            if 0 in self.comb_dict[0]:
                del self.comb_dict[0][0]
        if add_groups > 0:
            for x in range(add_groups):
                del self.comb_dict[1][0]

    def get_comb_key(self, sn) -> int:
        """get the starting key value for the comb dict for a session(sn)"""
        # get the min sess attendee number, unassigned attendee
        comb_key = min(self.sess_attendees[sn])

        # comb dict starting with the unassigned attendee must be greater than 0
        # and min_v must be less than number of sessions
        while len(self.comb_dict[comb_key]) == 0 and comb_key < cfg.n_sessions:
            comb_key += 1
            if comb_key not in self.comb_dict:
                # key 0 has been deleted
                comb_key = 0
                self.loop_cnt += 1

        return comb_key

    def build_missing_groups(self, sn, sg):
        """ build the remaining groups for a session
            sn = session number
            sg = list of groups for session
        """
        # get the min sess attendee number, unassigned attendee
        comb_key = self.get_comb_key(sn)

        # loop until all groups for session have be assigned or not satisfied after
        # max_loop attempts
        while len(sg) < cfg.n_groups and self.loop_cnt < self.max_loop:
            # scan comb list
            used_cg = []
            # get a group for the comb_dict
            for i, cg in enumerate(self.comb_dict[comb_key]):
                # ck member of group is not assigned
                good_group = True
                for e in cg:
                    if e not in self.sess_attendees[sn]:
                        good_group = False
                        break
                if good_group == True:
                    sg.append(cg)
                    used_cg.append(i)
                    self.update_sess_attendees(sn, cg)
                    # min_v = min(self.sess_attendees[sn])
                    break

            # remove used comb groups
            for ucgi in used_cg:
                del self.comb_dict[comb_key][ucgi]
            # set min_V for next loop
            comb_key += 1
            if comb_key not in self.comb_dict:
                # key 0 has been deleted
                comb_key = 0
                self.loop_cnt += 1
        print('')
        return

    def append_missed_attendees(self, s:int, a:list):
        """append missed attendee as new session group"""
        if len(a) == 0:
            pass
        elif len(a) < cfg.group_size:
            self.sessions[s].append(copy.copy(a))
        else:
            for i in range(0, len(a), cfg.group_size):
                self.sessions[s].append(sorted(a[i: i + cfg.group_size]))
        # remove attendees
        self.update_sess_attendees(s, copy.copy(a))

    def run(self,) -> None:
        """create the sessions"""
        log.info(f"beg {__name__}")
        self.sess_setup()
        self.gen_group_combinations()
        self.create_sessions()
        su.print_item(self.sessions, "sessions")
        log.info(f"end {__name__}")
