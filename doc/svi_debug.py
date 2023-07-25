#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  svi_debug.py
#
#  Copyright 2023 cswaim <cswaim@tpginc.net>

import sys
from itertools import combinations
import random
import math
from random import shuffle
import numpy as np
import time

sessions = {}
attendees = []
n_attendees = 9
n_groups = 3
group_size = 3
n_sessions = 4

def setup():
     """set the values"""
     global attendees, group_size
     attendees = [i for i in range(n_attendees)]
     group_size = math.floor(n_attendees / n_groups)

def first_session():
    """create first session"""
    subdiv_session = []
    session = attendees.copy()
    shuffle(session)
    for i in range(0, n_attendees, group_size):
        subdiv_session.append(sorted(session[i: i + group_size]))
    sessions[0] = subdiv_session
    return subdiv_session

def shuffle_between_groups(subdiv_session):
        """this function creates sessions 2 though n
        #form next small group (index group_after) by picking one member from each prior small group (index group_before)
        #shuffle movement between groups with Fisher-Yates"""

        group_before=[]
        for i in range(int(n_groups)):
            group_before.append(i)

        #shuffle(group_before)

        group_after = group_before.copy()

        #shuffle(group_after)

        print("group before", group_before)
        print("group after", group_after)

        new_group_session = [[] for j in range(n_groups)]
        #print('debug',int(num_attendees/sm_grp_size))

        #form next small group (index group_after) by picking one member from each prior small group (index group_before)
        for j in range(n_groups):
            #member number
            for i in range(group_size):
                # print(f'i={i}, j={j}, gb4_j={group_before[j]}')
                suffix = subdiv_session[group_before[j]][i]
                # print(f"gb4[{j}][{i}] = {suffix}")
                new_group_session[group_after[i]].append(suffix)

        return(new_group_session)

def print_parameters():
    """ print the parameters for at run"""
    print(f"no attendees: {n_attendees}")
    print(f"   no groups: {n_groups}")
    print(f"  group size: {group_size}")
    print(f"  n_sessions: {n_sessions}")
    print("")

def set_args():
    """get the command line args"""
    global n_attendees, n_groups, group_size, n_sessions
    print(sys.argv, len(sys.argv))
    valid_args = [4,5]
    if len(sys.argv) == 1:
        pass
    elif len(sys.argv) in valid_args:
        for i, a in enumerate(sys.argv):
           match i:
                case 1:
                    n_attendees = int(a)
                case 2:
                    n_groups = int(a)
                case 3:
                    group_size = int(a)
                case 4:
                    n_sessions = int(a)
    else:
        print('***')
        print("cmd args must be none or  include n_attendees, n_groups and group_size ")
        print('***')
        sys.exit()


if __name__ == '__main__':
    random.seed(4554)
    set_args()
    print_parameters()
    setup()
    in_sess = first_session()
    for i in range(1,n_sessions):
            #print('going in',in_sess)
            out_sess = shuffle_between_groups(in_sess)
            sessions[i] = out_sess.copy()
            print(f"group {i}  {out_sess} \n")
            in_sess = out_sess.copy()

    print(f"sessions:")
    for k,v in sessions.items():
         print(f"{k:02}  {v}")