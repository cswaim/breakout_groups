from collections import Counter 
import src.config as cfg
from src.card_child import CCard as Card
from src.sessions import Sessions

"""Conduct a event."""

class Event():
    """the event object"""

    def __init__(self, seed=None) -> None:
        self.all_card_interactions = []
        self.cards = []     # list of all card objects
        self.build_cards(cfg.n_attendees)
        self.sess = Sessions(seed=seed)
        self.sessions = self.sess.sessions
        self.interactions = self.sess.interactions
        #self.sess.build_sessions(seed)


    def build_cards(self, nc):
        for i in range(nc):
            self.cards.append(Card(i))

    def update_card_interactions(self, ):
        """ update individual card iteractions"""
        # k is session num,ber v is group list
        for k, v in self.sess.sessions.items():
            #
            #update_interact(list(chain.from_iterable(v)))

            # update card with group info, n grp num and g is group list of attendees
            for n, g in enumerate(v):
                upd_dict = self.cards[0].convert_grp_to_dict(g)
                for c in g:
                    self.cards[c].update_cards(upd_dict)
                    # set the group label, if label not found, use default
                    try:
                        glabel = cfg.group_labels[k][n]
                    except:
                        glabel = f"group{n}"
                    self.cards[c].update_sess_labels(glabel)

    def build_all_card_interactions(self,):
        """build a list of all the interactions from all cards """
        for c in self.cards:
            self.all_card_interactions.append(c.card_interactions)


    def get_interactions(self,all_cards=None):
        """Create dictionary of interactions among all attendees
           where the key is the card id.
        
        For every card id ...
           check for interaction with every other card id ...
              during every session.

        When an interaction between two cards
          in an a session group is found, record that in a counter.
        
        """
        interact = {}
        # For every person attending the event ...
        for person in all_cards:
            interact[person['name']] = []
            sessions = [k for k in person.keys() if "session" in k]

            # or possible interaction with every other person
            for person_other in all_cards:
                if person['name'] == person_other['name']:
                    continue

                # Will these two people meet in a session?
                # If so, store that in
                for session in sessions:
                    if person[session] == person_other[session]:
                        interact[person['name']].append(person_other['name'])

        return interact
    

    def show_cards(self,all_cards=None):
        # ToDo convert input to a pandas dataframe and
        # Should use pandas pretty printing for a dataframe

        # Print nice header

        # Each row is a card
        for row in all_cards.keys():
            print(row)

    def show_interactions_by_persons(self,all_cards=None):
        """For each person, list interactions with other persons."""
        result = self.get_interactions(all_cards=all_cards)
        # for k in result.keys():
        #     print(f"\n{k}")
        #     print(f"   {result[k]}\n") 

        pass
        for k in result.keys():
            simple_counts = Counter(result[k])
            sorted_counts = dict(sorted(simple_counts.items()))
            print(f"\n{k}")
            for person in sorted_counts.keys():
                print(f"   {person}:  {sorted_counts[person]}")


    def find_missing_persons(self):
        pass

    def find_multiple_encounters(self):
        pass

    def run(self, ):
        """run for event"""
        self.update_card_interactions()
        self.build_all_card_interactions()
