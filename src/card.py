"""Represents a card to sort attendees for each breakout.
    For every breakout session, the card specifies the group.
    the interactions counter captures how many times the attendee interacts with other attendees

"""

import random
from collections import Counter

class Card():
    """the card object"""

    def __init__(self, id) -> None:
        self.id = id
        self.sess_labels = []
        self.name = None
        self.breakout_groups = []
        self.card_interactions = Counter()

    def cards_for_event(self, 
                          n_attendees=None, 
                          n_groups=None,
                          grouping_algorithm=None):
        """Creates all the cards for the event."""
        all_cards_for_event = []
        for attendee_number in range(1, n_attendees + 1):
            card = Card(attendee_number)
            card.name = "Person" + str(attendee_number)
            session= {'name' : card.name}
            for breakout_group_number in range(1, n_groups + 1):
                session['session' + str(breakout_group_number)] = \
                    'group' + str(next(grouping_algorithm))
            all_cards_for_event.append(session)

        return all_cards_for_event
    
    def random_grouping_algorithm(self, n_groups=None, seed=None):
        # Placement in a group is from a uniformly distributed
        # randum num between 1 and the number of groups
        random.seed(seed)
        # get_config.config.getint('DEFAULT','attendees'):
        while True:
            yield random.randint(1,n_groups)

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

    def update_sess_labels(self, label) -> None:
        """append the label to the sess label list"""
        self.sess_labels.append(label)

    def print_the_cards_by_person(self, all_cards=None):
        " With catchy labels like continents, cars, and ski areas"
        for card in all_cards:
            print(card['name'])
            for session in card.keys():
                if 'session' in session:
                    print(f"   {session}: {card[session]}")


    def print_the_cards_by_session(self, all_cards=None):
        # Gather the persons by session

        # Show each session
        sessions = []
        for card in all_cards:
            for session in card.keys():
                if 'session' in session:
                    pass

        return None