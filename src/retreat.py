from src.card import Card
import pytest

"""Conduct a retreat."""

class Retreat():
    def __init__(self) -> None:
        pass

    def get_interactions(self,all_cards=None):
        """Create dictionary of interactions among all attendees
           where the key is the person.
        
        For every person ...
           check for interaction with every other person ...
              during every session.

        When an interaction between two persons
          in an a session is found, record that in a dict.
        
        """
        interact = {}
        # For every person attending the retreat ...
        for person in all_cards:
            interact[person['name']] = []
            sessions = [k for k in person.keys() if "session" in k]

            # or possible interaction with every other person
            for person_other in all_cards:
                if person['name'] == person_other['name']:
                    continue

                # Will these two people meet in a session?
                # If so, store that in
                for session in sessions:
                    if person[session] == person_other[session]:
                        interact[person['name']].append(person_other['name'])

        return interact


    def find_missing_persons(self):
        pass

    def find_multiple_encounters(self):
        pass


