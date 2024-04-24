
import copy
from src import config as cfg
from src import sessions_util as su
import logging
log = logging.getLogger(__name__)

"""
    Run parameters are passed in thru the config module
    Build session dictionary 1 thru x
    Populate session dictionary by the algorithm
    This base class creates the following instance attributes:
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

class SessionsAlgo():
    """ The sessions algorithm base class which establishes the breakout groups"""

    def __init__(self, seed=None, autorun=False):
        """init"""
        self.seed = seed
        su.set_seed(seed)
        self.groups = []
        self.sessions = su.init_sessions(cfg.n_sessions)
        self.interactions = {}
        # other instance variables for algorithm
        self.rand_attendees = copy.copy(cfg.attendees_list)

        # autorun the session
        if autorun:
            self.run()

    def build_sessions(self) -> dict:
        """build the sessions and return"""
        sessions = {0:[[1,2,3],[4,5,6],[7,8,9], [10,11]],
                    1:[[1,4,7,8],[2,5,11,12],[3,6,9], [10,13]],
                    2:[[1,5,9],[2,4,7],[3,6,8,10]],
                    3:[[2,4,6,8],[0,1,7],[3,5,9],[10]],
                    }

        return sessions

    def check_num_groups(self, sessions: list) ->list:
        """verify the number of groups in a session do not exceed cfg.n_groups
           and randomly distribute members to other groups"""
        for k, v in sessions.items():
            sessions[k] = su.assign_extra_attendees(v)
        return sessions

    def run(self,) -> dict:
        """ create the sessions
            This must create a self.sessions attribute and optionally, can create
            an interactions attribute
        """
        log.info("running sessions algo")
        new_sessions = self.build_sessions()
        self.sessions = self.check_num_groups(new_sessions)
