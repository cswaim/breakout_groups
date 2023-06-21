from collections import Counter

from src import config as cfg
import pandas as pd
from src.reports_interactions_matrix import InteractionsMatrix
import pytest

"""Unit tests for Interactions Matrix report."""

def test_build_interactions(config_event_defaults):
    rim = InteractionsMatrix()
    print('')
    result = rim.build_interactions()
    assert result[1][1] == 4

def test_gen_matrix(config_event_defaults, create_folders):
    rim = InteractionsMatrix()
    print('')
    df = rim.gen_matrix()
    # df is a class
    assert True == isinstance(df, pd.DataFrame)

    result = rim.print_matrix(df)
    with open(f'{cfg.datadir}interactions_reports.txt', 'w') as itxt:
        rim.print_matrix(df, fileobj=itxt)
    assert result == None

def test_hist(config_event_defaults, create_folders):
    rim = InteractionsMatrix()
    print("\n\n")
    result = rim.show_ascii_histogram()
    with open(f'{cfg.datadir}interactions_reports.txt', 'w') as itxt:
        rim.show_ascii_histogram(fileobj=itxt)
    assert result == None

