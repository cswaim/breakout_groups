""" Temp[late for the algorithm interface.

Import configuration information, like:
    from src import config as cfg

Include an "__init__" method, even if it is empty.

For INPUT:
Define a "run()" method with no parameters.

Within the run method execute your algorithm.

Output
Return an Event object.

See example below.
"""

from src import config as cfg
from src.event import Event

class AlgoInterface():

    def __init__(self):
        pass


    @classmethod
    def my_algorithm(cls):

        # Magic algorithm code goes here
        # When the algorithm finishes, its artifacts are placed in an Event
        algorithm_event = Event(seed='1234')
        algorithm_event.all_card_interactions = []
        algorithm_event.cards = []  

        return algorithm_event


    def run():
        print('/n')
        print("Hello from the algorithm run method")
        print(f"module name {cfg.sys_group_algorithm_class}")

        # Execute the algorithm here
        event = AlgoInterface.my_algorithm()

        return event
