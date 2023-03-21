from src.card import Card
import pytest

"""Conduct a retreat."""

class Retreat():
    def __init__(self) -> None:
        pass

    def get_interactions(self,all_cards=None):
        """Create dictionary of interactions among all attendees."""
        # Seed the dict with the person's name as the key
        breakpoint()
        interact = {}
        for person in all_cards:
            interact[person['name']] = []

            for person_other in all_cards:
                if person['name'] == person_other['name']:
                    
                    continue
                # Will these two people meet in a session?
                # If so, store that information
                if person.session1 == person_other.session1:
                    interact[person.name] = person_other.name

        breakpoint()
        return interact

    def find_missing_persons(self):
        pass

    def find_multiple_encounters(self):
        pass

    def create_inerations_dict():
        pass

