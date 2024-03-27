"""Represents a card to sort attendees for each breakout.
    For every breakout session, the card specifies the group.
    the interactions counter captures how many times the attendee interacts with other attendees

"""

import random
from collections import Counter
import src.config as cfg

class Card():
    """the card object"""

    def __init__(self, id) -> None:
        self.id = id
        self.group_labels = []
        self.name = None
        # self.breakout_groups = []
        self.card_interactions = Counter()
        # initialize counter
        for a in range(cfg.n_attendees):
            self.card_interactions[a] = 0

    def convert_grp_to_dict(self, group):
        """convert the group to a dict for the counter update
            [1,3,7] becomes {1:1, 3:1, 7:1} the key is the card number
                & the value is the interaction count
        """
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
        # set interactions with self to 0
        self.card_interactions[self.id] = 0
        no_opt = 0

    def update_group_labels(self, label) -> None:
        """append the label to the sess label list"""
        self.group_labels.append(label)

    def print_the_cards_by_person(self, all_cards=None) -> int:
        " print the cards by card id"
        card_cnt = 0
        for card in all_cards:
            card_cnt += 1
            print(card.id)
            for n, label in enumerate(card.group_labels):
                    print(f"   {cfg.session_labels[n-1]}: {label}")
        return card_cnt
