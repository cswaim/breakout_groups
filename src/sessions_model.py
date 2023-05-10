
import copy
from src import config as cfg

"""
    Run parameters are passed in thru the config module
    Build session dictionary 1 thru x 
    Populate session dictionary by the algorithm
    This module creates the following instance attributes:
        sessions: the sessions dictionary contains the outbreak sessions in the format
                {0:[[1,2,3],[4,5,6],[7,8,9]],
                 1:[[1,4,7],[2,5,8],[3,6,9]],
                 2:[[1,5,9],[2,4,7],[3,6,8]],
                }
        interactions:  OPTIONAL- the interactions dictionay is a dictionary of Counters, one for
            each attendee and is the count of times the attendee interacts with each other attendee.
            The reason this is optional, if it is calculated in the algorithm, then there is no
            need to recalc, but if the algorithm does not need it, then it is not required 

"""

class SessionsModel():
    """ The sessions algorithm which establishes the breakout groups"""

    def __init__(self, autorun=False):
        """init"""  
        self.groups = []
        self.sessions = {i:[] for i in range(0, cfg.n_sessions)}
        self.interactions = {}
        # other instance variables for algorithm
        self.rand_attendees = copy.copy(cfg.attendees_list)

        # autorun the session
        if autorun:
            self.run()

    def build_sessions(self) -> dict:
        """build the sessions and return"""
        sessions = {0:[[1,2,3],[4,5,6],[7,8,9]],
                    1:[[1,4,7],[2,5,8],[3,6,9]],
                    2:[[1,5,9],[2,4,7],[3,6,8]],
                    }
        return sessions
    
    def run(self,) -> dict:
        """ create the sessions
            This must create a self.sessions attribute and optionally, can create 
            an interactions attribute
        """
        self.sessions = self.build_sessions()
    