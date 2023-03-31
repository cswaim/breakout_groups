"""Represents a card to sort people for each breakout.
    Every card, just like every person, has a name.
    For every breakout session, the card specifies the group.

"""

import random
from collections import Counter

class Card():
    """the card object"""

    id = None
    name = None
    breakout_groups = []
    card_interactions = Counter()


    def __init__(self) -> None:
        self.name = None
        self.breakout_groups = []

    def cards_for_event(self, 
                          n_attendees=None, 
                          groups_per_session=None,
                          grouping_algorithm=None):
        """Creates all the cards for the event."""
        all_cards_for_event = []
        for attendee_number in range(1, n_attendees+1):
            card = Card()
            card.name = "Person" + str(attendee_number)
            session= {'name' : card.name}
            for breakout_group_number in range(1,groups_per_session+1):
                session['session'+str(breakout_group_number)] = \
                    'group'+str(next(grouping_algorithm))
            all_cards_for_event.append(session)

        return all_cards_for_event
    
    def random_grouping_algorithm(self, n_groups=None, seed=None):
        # Placement in a group is from a uniformly distributed
        # randum num between 1 and the number of groups
        random.seed(seed)
        # get_config.config.getint('DEFAULT','attendees'):
        while True:
            yield random.randint(1,n_groups)

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