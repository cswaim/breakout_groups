
from src import config as cfg
from src import sessions_util as su
import logging
log = logging.getLogger(__name__)


""" Methods to check if a group, or a session, are well formed.

From the issue:  https://github.com/cswaim/breakout_groups/issues/65

1. Every attendee is in a group. (All are present for the roll call).

2. No attended appears more than once in a group.

3.Groups do not exceed the configured size, although one may be smaller.
 The number of groups cannot exceed the n_groups from the cfg
this is because as a group planner, you establish the number of "rooms" that are available.
 Changing the n_groups means finding additional space which is not 
 always possible.

 
4. Groups are exactly the configured size, except when there are orphans, that
is, when the number of attendees is not excatly divible by the number of groups.
 if n_groups x n_group_size < n_attendees, then the groups can exceed the group_size.
if you have 3 groups of size 4 and 14 attendees, the two additional need to be assigned 
to an existing full group, but not the same group.  This is an example of placing
orphans in a group.

5. No more than one group has less than the configured number of attendees.  Not sure
what this rule means.
"""

class RollCall():

    """A class for performing roll call checks.

    This class provides a number of methods for checking the attendance of a group
    of people. The methods can be used to check if all attendees are present, 
    if no attendee is present in more than one group, and if the expected number 
    of groups are present.

    Attributes:
        None
    """

    def check_all_present(self, expected_attendees=None, session=None):
        """Is every attendee in a group?

        Args:
            expected_attendees: A list of the expected attendees.
            session: A list of groups of attendees.

        Returns:
            True if all attendees are present, False otherwise.
        """

        # compress the elements in the groups into a single list
        all_attendees_found_in_groups = su.groups_of_attendees_to_list(session=session)

        if len(expected_attendees) <= 0:
            return False

        for person in expected_attendees:
            if person not in all_attendees_found_in_groups:
                log.debug(f"{person} not in a group")
                return False

        return True

    def check_attendee_only_once(self, session=None):
        """No one is in the session more than once.

        This is logically equivalent to check if a person is
        scheduled to be in a group more than once, which physically will be difficult.

        Args:
            session: A list of groups of attendees.

        Returns:
            True if no attendee is present in more than one group, False otherwise.
        """

        all_attendees_found_in_groups = su.groups_of_attendees_to_list(session=session)

        for person in all_attendees_found_in_groups:
            if all_attendees_found_in_groups.count(person) > 1:
                return False

        return True

    def check_n_groups(self, expected_n_groups=None, session=None):
        """Are the expected number of groups in the session?

        Args:
            expected_n_groups: The expected number of groups.
            session: A list of groups of attendees.

        Returns:
            True if the expected number of groups are present, False otherwise.
        """

        if len(session) != expected_n_groups:
            return False

        return True

    def has_extra_elements(self, list_of_elements=None, list_of_lists=None):
        """Checks if the elements of a list are all contained in a list of lists.

        Args:
            list_of_elements: A list of elements to check.
            list_of_lists: A list of lists to check the elements against.

        Returns:
            True if any extra elements are found, False otherwise.
        """

        for element in list_of_elements:
            if not any(element in sublist for sublist in list_of_lists):
                return True

        return False

    def all_checks(self, expected_attendees=None,
                   expected_n_groups=None,
                   session=None):
        """Run all of the Roll Call checks instead of selected checks

        Args:
            expected_attendees: A list of the expected attendees.
            expected_n_groups: The expected number of groups.
            session: A list of groups of attendees.

        Returns:
            True if all of the Roll Call checks pass, False otherwise.
        """

        result = self.check_all_present(expected_attendees=expected_attendees,
                                          session=session)
        if not result: return False

        result = self.check_attendee_only_once(session=session)
        if not result: return False

        result = self.check_n_groups(expected_n_groups=expected_n_groups,
                                     session=session)
        if not result: return False

        return True
