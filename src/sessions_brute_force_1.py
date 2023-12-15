from src.sessions_model import SessionsModel
from src import sessions_returned as sr
from src import config as cfg

import random
import time
import logging
log = logging.getLogger(__name__)

"""Brute Force Algorithm number 1.

Attendees are selected randomly.
Previous interactions across sessions are not considered.
The coding's basic structure come from SeesionsModel
"""

class SessionsBruteForce1(SessionsModel):
    """ Use randomly chosen attendees to build sessions."""

    def build_sessions(self) -> dict:
        """Fills in all groups for a session, and builds all sessions.
        Your method "fill_in_a_group" obeys an algorithm to decide group membership.

        Args:
            None

        Returns:
            A SessionsReturns with all artifacts needed to analyze the run.
        """

        start_time = time.time()
        # Generate the list for attendees.  Should this be done in config?
        config_list_maker = cfg.ConfigParms()
        attendees_list = config_list_maker.gen_attendees_list()
        # For reproducing results it is handy to know the seed of random numbers
        rng = random.Random()
        random_seed = 13345
        rng.seed(random_seed)

        sessions_so_far = []
        made_sessions = 0
        while made_sessions < cfg.n_sessions:
            made_sessions +=1
            session = []

            made_groups = 0
            while made_groups < cfg.n_groups:
                made_groups +=1
                
                # Fill in a new group based on your algorithm
                new_group = self.fill_in_a_group(
                    attendees=attendees_list,
                    group_size=cfg.group_size,
                    session=session,
                    all_sessions=sessions_so_far)
                
                # Add this new group to the session
                session.append(new_group)

            # Session is full of groups 
            sessions_so_far.append(session)

        # Package all the vital info from this run and return it for analysis.
        values_for_this_run  = sr.SessionsReturned()
        values_for_this_run.seed = random_seed
        values_for_this_run.sessions = sessions_so_far
        end_time =time.time()

        elapsed_time = end_time - start_time
        print(f"\nElapsed time: {elapsed_time:.6f} seconds")
        values_for_this_run.elappsed = elapsed_time

        values_for_this_run.n_pairs_satisfied = None
        values_for_this_run.max_pairs = None
            
        values_for_this_run.n_attendees = cfg.n_attendees
        values_for_this_run.group_size = cfg.group_size
        values_for_this_run.n_groups = cfg.n_groups
        values_for_this_run.n_sessions = cfg.n_sessions
    
        return values_for_this_run
    

    def get_all_elements(self,
            list_of_lists=None) -> list:
        """Returns a list of all elements in a list of lists.
        Helper routine for working with sessions, which are lists of lists

        Args:
            list_of_lists: A list of lists.

        Returns:
            A list of all elements in the list of lists.
        """
        if list_of_lists == []:
            return []
        
        all_elements = []
        for sublist in list_of_lists:
            all_elements.extend(sublist)
        return all_elements


    def eligible_if_not_already_populated(self,
            attendees=None,
            session=None) -> list:
        """Returns a list of all attendees not already in the session.

        Args:
            attendees: A list of every attendee.
            session: A list of of the groups already populated in this session

        Returns:
            A list of all attendees which are eligible to be in a group, in this session.
        """

        # session is wide open, so return every attendee
        if session == [[]]:
            return attendees
       
        # No pool of eligible attendees, so return empty list
        if attendees == [] :
            return []
        
        already_in_session = self.get_all_elements(list_of_lists=session)
        eligable_set = set(attendees) - set(already_in_session)
        
        return list(eligable_set)
    

    def fill_in_a_group(self,
                        attendees=None,
                        group_size=None,
                        session=None, 
                        all_sessions=None) -> list:
        """Uses your algorithm to populate the attendees into a group.

            Args:
                attendees: A list of every attendee.
                group_size: Stop when this many attendees were added to group
                session: A list of of the groups already populated in this session
                all_sessions: May be useful fo an algorithm to see interactions
                
            Returns:
                The filled-in group as a list.
            """

        # Eliminate everyone already in the current session 
        candidates = self.eligible_if_not_already_populated(
                        attendees=attendees,
                        session=session)
        
        # Special case to populate the last group in the session.
        # The last group must consist of everyone who is left over.
        # if len(candidates) == group_size:
        #     return candidates
        
        new_group = self.your_algorithm_goes_here(
                        candidates=candidates,
                        group_size=group_size,
                        session=session,
                        sessions_so_far=all_sessions)
        
        return new_group
    
    def your_algorithm_goes_here(self,
                        candidates=None,
                        group_size=None, 
                        session=None,
                        sessions_so_far=None) -> list:
 
        """Uses an algorithm to populate the attendees into a group.
            Override this method with a call to a specifc algorithm.

        This algorithm just selects attendees at random.
        No consideration is made to interactions between attendees in
        prvious sessions.
        
        Args:
            candidates: A list of every attendee eligible to join the group
            group_size: Stop when this many attendees were added to group
            session: A list of of the groups already populated in this session

        Returns:
            The filled in group as a list.
        """
        new_group = []
        while len(new_group) < group_size:
            potential_group_member  = random.choice(candidates)
            if potential_group_member not in new_group:
                new_group.append(potential_group_member)

        return new_group
