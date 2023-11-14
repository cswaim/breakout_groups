import src.sessions_brute_force_1 as bf1
from src import config as cfg

import pytest

"""Test cases and helper methods for the algorithm brute_force_1"""

# Crude end-to-end systems test
def test_run_end_to_end():
    cfg.n_attendees = 16
    cfg.n_groups = 4
    cfg.group_size = 4
    cfg.n_sessions = 4
    bf = bf1.SessionsBruteForce1()
    sessions_returned = bf.build_sessions()
    assert sessions_returned.n_sessions == cfg.n_sessions
    assert sessions_returned.n_attendees == cfg.n_attendees
    print(f"\n")
    [print(session) for session in sessions_returned.sessions]


def test_eligible_if_not_already_populated():
        bf = bf1.SessionsBruteForce1()
        attendees = [0,1,2,3,4,5,6,7,8,9,10,11]
        session=[[0,1,2,3]]

        eligible = bf.eligible_if_not_already_populated( 
             attendees=attendees,
             session=session
        )
        assert eligible == [4, 5, 6, 7, 8, 9, 10, 11]


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
    bf = bf1.SessionsBruteForce1()
    for i in range(0,4):
        actual = bf.eligible_if_not_already_populated(
            attendees=attendees,
            session=sessions[i]
        )
        assert candidates[i] == actual