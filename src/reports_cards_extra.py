#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 cswaim <cswaim@tpginc.net

"""
After the sessions are built, for the set number of attendees, this module will generate x number of extra cards to allow for last minute sign-ups.
The number of extra cards is set by the cfg.n_extra_cards
"""
import os
import copy
from pathlib import Path
import logging
log = logging.getLogger(__name__)

from src import config as cfg
from src.card import Card
from src import sessions_util as su
from src import reports_util as rptu

class ReportsCardsExtra():
    """ After the sessions are built, for the set number of attendees,
        this module will generate x number of extra cards to allow
        for last minute sign-ups.
    The number of extra cards is set by the cfg.n_extra_cards
    """

    def __init__(self, autorun=False):
        """init"""
        # get a copy of sessions
        self.sessions = copy.copy(cfg.sessions)
        self.extra_cards = []
        for i in range(cfg.n_extra_cards):
            i += cfg.n_attendees
            self.extra_cards.append(Card(i))

        # init extra session {0: [[],[],[]...]}
        self.extra_sess = su.init_sessions(cfg.n_sessions)

        for k, v in self.extra_sess.items():
            sess_groups = []
            # check group size for override
            cfg.n_groups, cfg.group_size = su.set_n_groups(k)
            for a in range(cfg.n_groups):
                sess_groups.append([])
            self.extra_sess[k] = copy.deepcopy(sess_groups)

        # autorun the build
        if autorun:
            self.run()


    def add_extra_cards_to_group(self):
        """ get the max number in group
            for x in range(n_extra_card):
                loop thru groups for each session,
                    if group len < max number
                        add an extra person to group
            update the sessions in cfg
        """
        estats = rptu.calc_event_stats()
        max_group_size = estats["max_group_size"]

        # add each extra card id to each extra session
        for x in range(cfg.n_extra_cards):
            # session loop
            for k, v in self.sessions.items():
                min_len = min(len(grp) for grp in v)
                if min_len < max_group_size:
                    # get index of short group
                    n = v.index([grp for grp in v if len(grp) == min_len][0])
                    self.update_sess_group(x, k, n)
                else:
                    # all groups are same, append to first group
                    self.update_sess_group(x, k, 0)
                    # incr max group size when all are equal to spread assignment
                    max_group_size += 1

    def update_sess_group(self, x, k, n):
        """add the extra card to the sessions and exta_sess
            x=> card, k=> session, n=> group
        """
        self.extra_sess[k][n].append(self.extra_cards[x].id)
        self.sessions[k][n].append(self.extra_cards[x].id)

    def update_extra_cards_labels(self, ):
        """ update extra card labels"""
        # k is session number v is group list
        for k, v in self.extra_sess.items():
            # update card with group info, n grp num and g is group list of attendees
            for n, g in enumerate(v):
                upd_dict = self.extra_cards[0].convert_grp_to_dict(g)
                for c in g:
                    cinx = c - cfg.n_attendees
                    # set the group label, if label not found, use default
                    try:
                        glabel = cfg.group_labels[k][n]
                    except:
                        glabel = f"group{n}"
                    self.extra_cards[cinx].update_group_labels(glabel)


    def run(self,):
        """ run the addition of extra cards """
        log.info("add extra cards")
        self.add_extra_cards_to_group()
        self.update_extra_cards_labels()
        print()

if __name__ == '__main__':
    # set the config file working directory
    wkdir = str(Path(__file__).resolve().parent) + os.pathsep
    # set cfg default values for this test
    cfg.n_attendees = 11
    cfg.n_groups = 3
    cfg.group_size = 3
    cfg.n_sessions = 4
    cfg.n_extra_cards = 2
    cfg.sessions = {
        0 : [[1, 7, 9, 3], [0, 5, 6], [2, 4, 8, 10]],
        1 : [[7, 8, 10], [3, 6, 9, 0], [1, 4, 5, 2]],
        2 : [[3, 5, 9, 0], [1, 2, 7], [4, 6, 8, 10]],
        3 : [[2, 4, 6, 8], [0, 1, 7], [3, 5, 9, 10]],
        }
    rce = ReportsCardsExtra(autorun=True)
    print(rce.extra_sess)
    print(rce.sessions)
    for c in rce.extra_cards:
        print(c.id, c.group_labels)