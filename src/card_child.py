#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>
 
from src.card import Card
class CCard(Card):
    """ child card """ 

    def __init__(self, id) -> None:
        super().__init__()
        self.id = id
        self.sess_labels = []
 
    def convert_grp_to_dict(self, group):
        """convert the group to a dict for the counter update"""
        # build update dict
        upd_dict ={}
        for x in group:
            upd_dict[x] = 1
        return upd_dict

    def update_cards(self, upd_dict):
        """update an individual card interactions from a group formated as dic"""
        if type(upd_dict) != dict:
            upd_dict = self.convert_grp_to_dict(upd_dict)
        self.card_interactions.update(upd_dict)

    def update_sess_labels(self, label) -> None:
        """append the label to the sess label list"""
        self.sess_labels.append(label)

