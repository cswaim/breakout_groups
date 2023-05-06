import random
import copy
from src import config as cfg

"""
    Build session dictionary 1 thru x 
    Populate session dictionary by shuffling the attendees list
    This module creates the following attributes:
        the sessions dictionary contains the outbreak sessions
        Optional: the interactions dictionay is a Counters, one for each attendee and
                  is the count of 

"""


class SessionsModel():
    """ The sessions algorithm which establishes the breakout groups"""

    def __init__(self, autorun=True):
        """init"""  
        self.groups = []
        self.sessions = {i:[] for i in range(0, cfg.n_sessions)}
        self.interactions = {}
        self.rand_attendees = copy.copy(cfg.attendees_list)
        if autorun:
            self.run()

    def run(self,) -> dict:
        """ create the sessions
            This must create a self.sessions attribute and optionally, can create 
            an interactions attribute
        """
        self.sessions = {0:[[1,2,3],[4,5,6],[7,8,9]],
                        1:[[1,4,7],[2,5,8],[3,6,9]],
                        2:[[1,5,9],[2,4,7],[3,6,8]],
                        }
    