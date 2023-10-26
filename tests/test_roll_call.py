import src.roll_call as rc
from src import sessions_util as su
from src import config as cfg

import pytest

# Every attendee is in a group. (All are present for the roll call).
def test_check_all_present():
    """Check that every attendee is in a group somewhere."""
    rc_checker = rc.RollCall()
    # Populate groups based on the attendee_list and number of groups.

    n_attendees=12
    event = su.make_sessions_returned(n_attendees=n_attendees,
                                group_size=4,n_sessions=4)

    session = event.sessions[0]
    attendee_list = list(range(0,n_attendees))
    for session in event.sessions:
        assert rc_checker.check_all_present(expected_attendees=attendee_list, 
                                            session=session)
        

# No attendee appears more than once in a group.  Happy Day
def test_only_once():
    rc_checker = rc.RollCall()
    event = su.make_sessions_returned(n_attendees=12,
                                group_size=4,n_sessions=4)
    for session in event.sessions:
        assert rc_checker.check_attendee_only_once(session=session)


@pytest.mark.xfail
def test_is_element_in_list_of_lists_more_than_once_fail():
    rc_checker = rc.RollCall()
    n_attendees = 30
    group_size = 5
    event = su.make_sessions_returned(n_attendees=n_attendees,
                            group_size=group_size,n_sessions=4)
    # To the first session, first group, duplicate the second  attendee
    event.sessions[0][0][0] = event.sessions[0][0][1]
    for session in event.sessions:
        assert rc_checker.check_attendee_only_once(session=session)


# Numbe of groups is as expected
def test_check_n_groups():
    rc_checker = rc.RollCall()
    n_attendees = 65
    group_size = 5
    computed_n_groups = n_attendees / group_size
    event = su.make_sessions_returned(n_attendees=n_attendees,
                            group_size=group_size,n_sessions=4)
    for session in event.sessions:
        assert rc_checker.check_n_groups(expected_n_groups=computed_n_groups,
                                          session=session)


@pytest.mark.parametrize("list_of_elements, list_of_lists, expected_result", [
  ([1, 2, 3, 4, 5, 6], [[1, 2, 3], [4, 5, 6]], False),
  ([1, 2, 3, 4, 5, 6, 7], [[1, 2, 3], [4, 5, 6]], True),
  ([], [], False)
])
def test_has_extra_elements(list_of_elements, list_of_lists, expected_result):
    rc_checker = rc.RollCall()
    actual_result = rc_checker.has_extra_elements(list_of_elements=list_of_elements,
                                                   list_of_lists=list_of_lists)
    assert actual_result == expected_result


# All the tests with no orphans
# @pytest.mark.skip
def test_all_checks():
    """Correct groups within a correct session"""
    reference = list(range(1, cfg.n_attendees+1))
    expected_n_groups = 3
    session = [[1,2,3,4], [5,6,7,8], [9,10,11,12]]
    rc_checker = rc.RollCall()
    assert rc_checker.all_checks(expected_attendees=reference, 
                                 expected_n_groups=expected_n_groups,
                                 session=session)


# ToDO:  Need tests when the sessions have some orphans
