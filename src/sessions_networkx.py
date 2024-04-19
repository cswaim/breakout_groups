import logging
import time
import random
import networkx as nx
import matplotlib.pyplot as plt

# from src.sessions_brute_force_1 import SessionsBruteForce1
from src.sessions_model import SessionsModel
from src import sessions_returned as sr
from src import config as cfg

log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
# file_handler = logging.FileHandler(cfg.datadir + 'SessionsNetworkx.log')
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)
# log.addHandler(file_handler)

"""Brute Force Algorithm number 3.
Attendees are selected based on previous interactions in the session.
The  basic structure comes from SessionsModel.
"""


class SessionsNetworkx(SessionsModel):
    """A framework for different algorithms for filling in groups.

    Interactions between attenddes are stored as a network.
    Node: Attendee
    Edge: Indicates and interaction.  No edge between nodes means no interactions

    BFI is responsible for filling each session, and for filling all sessions.
    This class contains the algorithm for filling one group.
    The method "your_algorithm_goes_here" overrides the one in BF1.

    """

    def __init__(self, seed=None, autorun=False):
        """init"""
        super().__init__(seed, autorun)
        self.network = nx.Graph()
        # Populate the nodes in the network, based on the attendees
        self.populate_nodes_in_network()

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
        # config_list_maker = cfg.ConfigParms()
        # attendees_list = config_list_maker.gen_attendees_list()
        attendees_list = cfg.attendees_list
        # For reproducing results it is handy to know the seed of random numbers
        rng = random.Random()
        # random_seed = 13345
        rng.seed(cfg.random_seed)

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
        values_for_this_run.seed = cfg.random_seed
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

        # session interface requires a dict
        sess_dict = {i: v for i, v in enumerate(sessions_so_far)}
        # return values_for_this_run
        self.sessions_returned = values_for_this_run
        return sess_dict


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

        """This algorithm just selects attendees by considering
            interactions between attendees in previous sessions.

        Args:
            candidates: A list of every attendee eligible to join the group.
            group_size: Stop when this many attendees were added to group
            session: current session.  May have groups already formed.
            sessions_so_far: Not used.  Interaction information is in network.


        Returns:
            The filled in group as a list.
        """

        # Intialize the first element in the new group
        # group_so_far = self.get_initial_member(network=self.network,
        #                                         session=session)
        group_so_far = []

        # Add members to the group until it is full.
        while len(group_so_far) < group_size:
            log.debug('Adding members to group_so_far')
            new_member = self.get_next_member(network=self.network,
                session=session,
                group_so_far=group_so_far)

            # Add the member to the group.
            group_so_far.append(new_member)

            # Add an edge from this new member node to everyone else in the group
            for attendee in group_so_far:
                if attendee != new_member:
                    self.network.add_edge(attendee,new_member)

        return group_so_far


    def get_next_member(self, network=None, session=None, group_so_far=None):
        """
        Get the next eligible member for the session.

        Parameters:
        - self: The instance of the class.
        - network: The network from which to select the next member.
        - session: The current session, a list of groups.
        - group_so_far: The groups formed so far.

        Returns:
        - The next eligible member for the group.

        Notes:
        - Anyone already in the session is no longer eligible for future groups.
        The 'not_eligible' list is used to filter out such members.

        """
        log.info(f'    group_so_far:  {group_so_far}')
        # Anyone already in the session is no longer eligible for future groups.
        not_eligible = [attendee for group in session for attendee in group]
        log.info(f' {len(not_eligible)}  not_eligibale initial: {not_eligible}')

        # Anyone already in this group should not be considered again.
        for attendee in group_so_far:
            not_eligible.append(attendee)
        not_eligible = list( set(not_eligible))
        log.info(f'   {len(not_eligible)} final list of not_eligible:  {not_eligible}')

        # find the set of everyone eligible, based on prior not being a member
        all_attendees = network.nodes()
        eligible = list (set(all_attendees) - set(not_eligible)  )

        # In theory, there should always be at least one eligible attendee because
        #    not everyone has been assigned yet.
        if len(eligible) == 0:
            log.error("No one is eligible!")
            log.error(f"   group_so_far:  {group_so_far}")
            log.error(f"   session: {session}")
            log.error(f"   not:eligible: {not_eligible}")
            member =  None

        elif len(eligible) == 1:
            log.info(f"   eligible is == 1 so picking it.  {eligible}")
            log.info(f"   not_eligible is:  {not_eligible}")
            member = eligible[0]

        else :
            # Find a node that is a.) eligible, and b.) has the smallest number of
            # edges to the nodes in the group being formed.
            # Find all the neighbors for all the nodes already in the group.
            neighbors = set([])
            for attendee in group_so_far:
                neighbors = neighbors.union(set(self.network.neighbors(attendee)))

            # Find a node that is not a neighbor
            candidates = list ( set(eligible) - set(neighbors))
            if len(candidates) == 0:
                member = eligible[0]
            else:
                # Pick one
                member = candidates[0]

        return member

    def populate_nodes_in_network(self):
        # Initially there are no edges, because there have been no interactions
        nodes = list(range(0,cfg.n_attendees))
        self.network.add_nodes_from(nodes)


    def plot_network(self):
        # Draw the graph.  Close it manually.
        return
        pos = nx.spring_layout(self.network)
        nx.draw(self.network, pos, with_labels=True, node_color='skyblue')
        plt.show()

