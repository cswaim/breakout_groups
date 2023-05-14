from collections import Counter

#from src import config as cfg
from src.reports_interactions_matrix import InteractionsMatrix
import pytest

"""Unit tests for Interactions Matrix report."""

def test_build_interactions(config_event_defaults):
    rim = InteractionsMatrix()
    print('')
    result = rim.build_interactions()
    assert result[1][1] == 4

def test_gen_matrix(config_event_defaults):
    rim = InteractionsMatrix()
    print('')
    result = rim.run()
    assert result == None

