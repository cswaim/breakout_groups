from collections import Counter as counter
from src.card import Card
from src.sessions_random import Sessions

"""Conduct a event."""

class Event():
    """"""

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
        # For every person attending the event ...
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


    def show_cards(self,all_cards=None):
        # ToDo conver input to a pandas dataframe and
        # Use pandas pretty printing for a dataframe

        # Print nice header


        # Each row is a card
        for row in all_cards.keys():
            pass

    def show_interactions_by_persons(self,all_cards=None):
        """For each person, list interactions with other persons."""
        result =self.get_interactions(all_cards=all_cards)
        # for k in result.keys():
        #     print(f"\n{k}")
        #     print(f"   {result[k]}\n") 

        pass
        for k in result.keys():
            simple_counts = counter(result[k])
            sorted_counts = dict(sorted(simple_counts.items()))
            print(f"\n{k}")
            for person in sorted_counts.keys():
                print(f"   {person}:  {sorted_counts[person]}")

    

    def find_missing_persons(self):
        pass

    def find_multiple_encounters(self):
        pass


