"""
   Specifies an interface for sessions returned by an algorithm.
"""
class SessionsReturned():
    def __init__(self):

        # The seed for random numbers used by the algorithm.
        self.seed = None

        # A session is a list of groups.
        # Within a group is a list of attendees
        self.sessions = None

        # Time required to create the sessions, in sec onds
        self.elappsed = None

        # Where appropriate, the number of pairs satisfied
        self.n_pairs_satisfied = None

        # Where appropriate, max_pairs
        self.max_pairs = None
        