import logging
import networkx as nx
import matplotlib.pyplot as plt

from src.sessions_brute_force_1 import SessionsBruteForce1
from src import config as cfg

log = logging.getLogger('SessionsNetworkx')
log.setLevel(logging.WARNING)
file_handler = logging.FileHandler(cfg.datadir + 'SessionsNetworkx.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
log.addHandler(file_handler)

"""Brute Force Algorithm number 3.
Attendees are selected based on previous interactions in the session.
The  basic structure comes from SessionsModel.
"""


class SessionsNetworkx(SessionsBruteForce1):
    """A framework for different algorithms for filling in groups.

    Interactions between attenddes are stored as a network.
    Node: Attendee
    Edge: Indicates and interaction.  No edge between nodes means no interactions

    BFI is responsible for filling each session, and for filling all sessions.
    This class contains the algorithm for filling one group.
    The method "your_algorithm_goes_here" overrides the one in BF1.

    """

    def __init__(self):
        self.network = nx.Graph()
        # Populate the nodes in the network, based on the attendees
        self.populate_nodes_in_network()


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
        pos = nx.spring_layout(self.network)
        nx.draw(self.network, pos, with_labels=True, node_color='skyblue')
        plt.show()

