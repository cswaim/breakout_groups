from  src.sessions_networkx import SessionsNetworkx
from src.roll_call import RollCall
from src import config as cfg

import pytest

"""Test cases and helper methods for the algorithm brute_force_1"""

# Crude end-to-end systems test
def test_run_end_to_end():
    cfg.n_attendees=16
    cfg.group_size = 4
    cfg.n_groups = 4
    cfg.n_sessions = 5

    snx = SessionsNetworkx()
    sessions_returned = snx.build_sessions()

    print(f"\n")
    print(f"\nElapsed time: {sessions_returned.elappsed:.6f} seconds")
    [print(session) for session in sessions_returned.sessions]

    for node in snx.network.nodes:
        print(f"Node {node} has degree {snx.network.degree(node)}  and neighbors {list(snx.network.neighbors(node))}")


@pytest.mark.skip(reason="if not run manually, will freeze until plot window closed.")
# Draw the network graph
def test_plot_network():
    cfg.n_attendees=16
    cfg.group_size = 4
    cfg.n_groups = 4
    cfg.n_sessions = 2

    snx = SessionsNetworkx()
    # Build the newtork as a side effect of creating the sessions
    sessions_returned = snx.build_sessions()
    snx.plot_network()

def test_show_neighbors():
    cfg.n_attendees = 16
    cfg.group_size = 4
    cfg.n_groups = 4
    cfg.n_sessions = 2

    snx = SessionsNetworkx()
    sessions_returned = snx.build_sessions()
    assert sessions_returned

    for node in snx.network.nodes:
        print(f"Node {node} has degree {snx.network.degree(node)}  and neighbors {list(snx.network.neighbors(node))}")


# @pytest.mark.skip(reason="empty eligibility list.  Need to debug.")
#   simulate an actual Retreat
def  test_simulate_retreat():
    cfg.n_attendees = 30
    cfg.group_size = 5
    cfg.n_groups = 6
    cfg.n_sessions = 2

    snx = SessionsNetworkx()
    sessions_returned = snx.build_sessions()
    assert sessions_returned

    for node in snx.network.nodes:
        print(f"Node {node} has degree {snx.network.degree(node)}  and neighbors {list(snx.network.neighbors(node))}")
    

    [print(session) for session in sessions_returned.sessions]
