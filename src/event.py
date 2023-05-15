from collections import Counter 
from itertools import chain
import src.config as cfg
from src.card import Card
from src.sessions import Sessions
from src.reports import Reports

"""Conduct a event."""

class Event():
    """the event object"""

    def __init__(self, seed=None) -> None:
        self.all_card_interactions = {}
        self.all_cards = []     # list of all card objects
        self.init_cards(cfg.n_attendees)
        # instantiate class
        self.sess = Sessions(seed=seed, autorun=True)
        self.sessions = self.sess.sessions
        self.interactions = self.sess.interactions

    def init_cards(self, nc):
        for i in range(nc):
            self.all_cards.append(Card(i))

    def update_cards(self, ):
        """ update individual card iteractions and labels"""
        # k is session num,ber v is group list
        for k, v in self.sess.sessions.items():
            #
            #update_interact(list(chain.from_iterable(v)))

            # update card with group info, n grp num and g is group list of attendees
            for n, g in enumerate(v):
                upd_dict = self.all_cards[0].convert_grp_to_dict(g)
                for c in g:
                    self.all_cards[c].update_cards(upd_dict)
                    # set the group label, if label not found, use default
                    try:
                        glabel = cfg.group_labels[k][n]
                    except:
                        glabel = f"group{n}"
                    self.all_cards[c].update_sess_labels(glabel)

    def build_all_card_interactions(self,):
        """build a list of all the interactions from all cards """
        for c in self.all_cards:
            self.all_card_interactions[c.id] = c.card_interactions   

    def show_cards(self,all_cards=None):
        # ToDo convert input to a pandas dataframe and
        # Should use pandas pretty printing for a dataframe

        # Print nice header

        # Each row is a card
        for row in all_cards.keys():
            print(row)

    def show_interactions_by_persons(self,):
        """For each person, list interactions with other persons."""
        result = self.all_card_interactions
        for k, v in self.all_card_interactions.items():
            interact = []
            for i in range(cfg.n_attendees):
                interact.append(f"{i}:{v[i]}")
            print(f"{k}:  {interact}") 

        self.show_sessions()
    
    def show_sessions(self,):
        """list the sessions"""
        for i, val in self.sessions.items():
            print(f"Session {i:02} - {val}")


    def find_missing_persons(self):
        pass

    def find_multiple_encounters(self):
        pass

    def set_cfg_variables(self,):
        """set the cfg variables for passing to reports"""
        cfg.all_card_interactions = self.all_card_interactions
        cfg.all_cards = self.all_cards
        cfg.sessions = self.sessions

    def gen_reports(self):
        """generate the reports for this event"""
        rpt = Reports(autorun=True)

    def run(self, ):
        """run for event"""
        self.update_cards()
        self.build_all_card_interactions()
        self.set_cfg_variables()
        self.gen_reports()
