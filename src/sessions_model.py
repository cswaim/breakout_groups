
import copy
from src import config as cfg
from src.sessions_algo import SessionsAlgo
from src import sessions_util as su
import logging
log = logging.getLogger(__name__)

"""
    This model shows an implementation of the sessions_algo class

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

class SessionsModel(SessionsAlgo):
    """ The sessions algorithm which establishes the breakout groups"""

    def __init__(self, seed=None, autorun=False):
        """init"""
        super().__init__(seed, autorun)

        # allow group_size to be overridden by session
        self.group_size = cfg.group_size
        # autorun the session
        if autorun:
            self.run()

    def build_sessions(self) -> dict:
        """build the sessions and return"""
        self.group_size = su.set_group_size()
        sessions = {0:[[1,2,3],[4,5,6],[7,8,9], [10,11]],
                    1:[[1,4,7],[2,5,8],[3,6,9], [10,11,12,13]],
                    2:[[1,5,9],[2,4,7],[3,6,8]],
                    3:[[2,4,6,8],[0,1,7],[3,5,9,10]],
                    }
        return sessions

