from src.sessions_random import Sessions

from collections import Counter
from itertools import combinations

"""Utilities for organizing and showing Sessions objects"""
class SessionsUtils():
    """Create dict of interactions amon attendees"""
    def get_session_interactions(session=None):

        sc = session
        #  Generate random groups for each session
        sc.build_sessions()
        

        # Combinations of attendees will be the dict keys.
        sc.rand_attendees.sort()
        sc_combos = list(combinations(sc.rand_attendees,2))

        # for easier reading, convert tuples to strings.
        # The notation "1-2" means "1 and 2 were in the same group."
        # Also, the notation "1-2" means "2 and 1 were in the same group."
        readable_combos  = [str(e[0]) +'_' + str(e[1]) for e in sc_combos]

        # A data structure to tally the frequency of each interaction.
        interactions = {k:0 for k in readable_combos}

        # In a group there are combinations of interactions.  
        # Tally the frequency of each interaction
        
        # breakpoint()
        for session in range(1,len(sc.sessions)):
            for a_group in sc.sessions[session]:
                    a_group.sort()
                    combos = list(combinations(a_group,2))
                    readables  = [str(e[0]) +'_' + str(e[1]) for e in combos]
                    for an_interaction in readables:
                        interactions[an_interaction] +=1

        return interactions
    
    """Simple horizontal histogram of attendee interactions"""
    def show_ascii_histogram(interactions=None):
        # COunt the number of interactions that have a alue of 
        # 0, 1, etc
        # Crete a simple histogram to show the distribution
        # breakpoint()
        rows = Counter(interactions.values())
        print("\n")
        for row in sorted(rows):
             print(f"{row}  {rows[row]}    {'*' * rows[row]} ")
        pass
