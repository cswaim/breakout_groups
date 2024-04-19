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
    reference= list(range(0, cfg.n_attendees))

    snx = SessionsNetworkx()
    sessions = snx.build_sessions()
    sessions_returned = snx.sessions_returned

    print(f"\n")
    print(f"\nElapsed time: {sessions_returned.elappsed:.6f} seconds")
    [print(session) for session in sessions_returned.sessions]

    for node in snx.network.nodes:
        print(f"Node {node} has degree {snx.network.degree(node)}  and neighbors {list(snx.network.neighbors(node))}")

    rc = RollCall()
    for a_session in sessions_returned.sessions:
        assert rc.all_checks(expected_attendees=reference,
                    expected_n_groups=cfg.n_groups,
                    session=a_session)


@pytest.mark.skip(reason="if not run manually, will freeze until plot window closed.")
# Draw the network graph
def test_plot_network():
    cfg.n_attendees=16
    cfg.group_size = 4
    cfg.n_groups = 4
    cfg.n_sessions = 2

    snx = SessionsNetworkx()
    # Build the newtork as a side effect of creating the sessions
    sessions = snx.build_sessions()
    sessions_returned = snx.sessions_returned
    snx.plot_network()

def test_show_neighbors():
    cfg.n_attendees = 16
    cfg.group_size = 4
    cfg.n_groups = 4
    cfg.n_sessions = 2
    reference= list(range(0, cfg.n_attendees))

    snx = SessionsNetworkx()
    sessions = snx.build_sessions()
    sessions_returned = snx.sessions_returned
    assert sessions_returned

    for node in snx.network.nodes:
        print(f"Node {node} has degree {snx.network.degree(node)}  and neighbors {list(snx.network.neighbors(node))}")

    rc = RollCall()
    for a_session in sessions_returned.sessions:
        assert rc.all_checks(expected_attendees=reference,
                    expected_n_groups=cfg.n_groups,
                    session=a_session)


# @pytest.mark.skip(reason="empty eligibility list.  Need to debug.")
#   simulate an actual Retreat
def  test_simulate_retreat():
    cfg.n_attendees = 30
    cfg.group_size = 5
    cfg.n_groups = 6
    cfg.n_sessions = 2

    snx = SessionsNetworkx()
    sessions = snx.build_sessions()
    sessions_returned = snx.sessions_returned
    assert sessions_returned

    for node in snx.network.nodes:
        print(f"Node {node} has degree {snx.network.degree(node)}  and neighbors {list(snx.network.neighbors(node))}")


    [print(session) for session in sessions_returned.sessions]

    reference= list(range(0, cfg.n_attendees))
    rc = RollCall()
    for a_session in sessions_returned.sessions:
        assert rc.all_checks(expected_attendees=reference,
                    expected_n_groups=cfg.n_groups,
                    session=a_session)

@pytest.mark.skip(reason="eliminate brute force class")
def test_eligible_if_not_already_populated():
        bf = SessionsNetworkx()
        attendees = [0,1,2,3,4,5,6,7,8,9,10,11]
        session=[[0,1,2,3]]

        eligible = bf.eligible_if_not_already_populated(
             attendees=attendees,
             session=session
        )
        assert eligible == [4, 5, 6, 7, 8, 9, 10, 11]

@pytest.mark.skip(reason="eliminate brute force class")
# Happy day, empty lists, various sizes, invalid types for parameters, etc.
def test_eligible_if_not_already_populated_param():
    attendees = [0,1,2,3,4,5,6,7,8,9,10,11]
    sessions = [ [[]],
            [[11,10,9,8]],
            [[0,1,2,3],[4,5,6,7]],
            [[0,1,2,3], [4,5,6,7], [8,9,10,11]]
    ]
    candidates = [
    [0,1,2,3,4,5,6,7,8,9,10,11],
    [0,1,2,3,4,5,6,7],
    [8,9,10,11],
    []
    ]
    bf = SessionsNetworkx()
    for i in range(0,4):
        actual = bf.eligible_if_not_already_populated(
            attendees=attendees,
            session=sessions[i]
        )
        assert candidates[i] == actual