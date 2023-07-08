
from itertools import combinations
import random
from random import shuffle
import numpy as np
import time
import copy
from src import config as cfg
import logging
log = logging.getLogger(__name__)

"""

"""

class SessionsVerticalIntersection():
    """ The sessions algorithm which establishes the breakout groups"""

    def __init__(self, seed=None, autorun=False):
        """init"""
        self.seed = seed
        self.groups = []
        self.sessions = {i:[] for i in range(0, cfg.n_sessions)}
        self.interactions = {}
        # other instance variables for algorithm
        self.rand_attendees = cfg.attendees_list.copy()

        # autorun the session
        if autorun:
            self.run()

    def shuffle_session(self, num_attendees, sm_grp_size):
        """ this function creates a randomized first session"""

        session=[]
        for i in range(num_attendees):
            session.append(i)
        shuffle(session)
        subdiv_session=[[] for j in range(int(num_attendees/sm_grp_size))]
        for i in range(int(num_attendees/sm_grp_size)):
            for j in range(sm_grp_size):
                subdiv_session[i].append(session[j+i*(sm_grp_size)])

        #print(session, subdiv_session)

        return(subdiv_session)

    def shuffle_between_groups(self, subdiv_session):
        """this function creates sessions 2 though n
        #form next small group (index group_after) by picking one member from each prior small group (index group_before)
        #shuffle movement between groups with Fisher-Yates"""

        group_before=[]
        for i in range(int(cfg.n_attendees/cfg.group_size)):
            group_before.append(i)

        shuffle(group_before)

        group_after = group_before.copy()
    #    # using Fisher–Yates shuffle Algorithm
    #    # to shuffle a list
    #    for i in range(len(group_after)-1, 0, -1):
    #        # Pick a random index from 0 to i
    #        #j = random.randint(0, i + 1)
    #        j=random.randint(0, i)
    #        # Swap loc[i] with the element at random index
    #        group_after[i], group_after[j] = group_after[j], group_after[i]

        shuffle(group_after)

        print("group before", group_before)
        print("group after", group_after)

        new_group_session=[[] for j in range(int(cfg.n_attendees/cfg.group_size))]
        #print('debug',int(num_attendees/sm_grp_size))


        #form next small group (index group_after) by picking one member from each prior small group (index group_before)
        for j in range(len(group_before)):
            #member number
            for i in range(len(group_before)):
                #print('i,j,group_before[j]',i,j,[group_before[j]])
                suffix=subdiv_session[group_before[j]][i]
                new_group_session[group_after[i]].append(suffix)
        return(new_group_session)


    def flatten_retreat(self, whole, attendees):
        """"""
        max_pairs=len(list(combinations(attendees,2)))

        flatter_list = [item for sublist in whole for item in sublist]
        #flattest_list = [item for sublist in flatter_list for item in sublist]
        #print(flatter_list)
        return(len(flatter_list),max_pairs)

    def pop_non_interactions(self, session, sm_grp_size, non_interactions):
        """ this function removes interactions from given session comprehensive list of interactions (non_interactions remain)
        """
        for i in range(sm_grp_size):
            pairs=list(combinations(session[i],2))
            for j in range(len(pairs)):
                rev_pair=(pairs[j][1],pairs[j][0])
                #print('forward/rev',pairs[j],rev_pair)
                if pairs[j] in non_interactions:
                    #print('found',pairs[j])
                    non_interactions.pop(non_interactions.index(pairs[j]))
                elif rev_pair in non_interactions:
                    #print('reverse found',pairs[j])
                    non_interactions.pop(non_interactions.index(rev_pair))
                #else:
                    #print('redundant interaction for', pairs[j])
                #print('length of non_interactions',len(non_interactions))
        return(non_interactions)

    def build_sessions(self,):
        end=time.time()
        start = time.time()


        #artifact of network design where there is a 1:1 map between group size and number of groups
        #could carry an extra variable and say "num_attendees=sm_grp_size*num_grps"

        #create a set that contains all attendees
        attendees=set(range(cfg.n_attendees))

        #initialize a running tally of non interactions
        non_interactions=list(combinations(attendees,2))


        print('small_group_size = number_of_small_groups= ',cfg.group_size)
        print('number of attendees <= ',cfg.n_attendees)
        input = self.shuffle_session(cfg.n_attendees, cfg.group_size)

        non_interactions = self.pop_non_interactions(input, cfg.group_size, non_interactions)

        whole_retreat=[]
        whole_retreat.append(input)
        elapsed = end - start
        print('group',0,input,'% 6.4f sec,' % elapsed)


        for i in range(1,10):
            #print('going in',input)
            output = self.shuffle_between_groups(input)
            whole_retreat.append(output)
            non_interactions = self.pop_non_interactions(output, cfg.group_size, non_interactions)
            end=time.time()
            elapsed = end - start
            (length,max_pairs)= self.flatten_retreat(whole_retreat,attendees)
            print('group',i,output,'% 6.4f sec,' % elapsed,length,'groups,',max_pairs-len(non_interactions),'/',max_pairs,'pairs satisfied')
            input = output.copy()

        return whole_retreat

    def run(self, ) -> dict:
        """ create the sessions
            This must create a self.sessions attribute and optionally, can create
            an interactions attribute
        """
        log.info(f"beg {__name__}")
        cfg.group_size=4
        cfg.n_attendees=cfg.group_size*cfg.group_size

        self.sessions = self.build_sessions()
        log.info(f"end {__name__}")



# if __name__ == '__main__':
#     """ create breakout goups for an event"""
#     # get the cfg parameters
#     cfg.cp.run()

#     svi = SessionsVerticalIntersection(seed=3331)
#     svi.run()