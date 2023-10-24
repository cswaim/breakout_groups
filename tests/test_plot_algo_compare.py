from collections import Counter

import datetime
from pathlib import Path
import src.config as cfg
from src.plot_algo_compare import PlotAlgoCompare
import pytest

"""Unit tests for plot algo compare"""

def test_build_plot_file_name(config_event_defaults):
    """test building of all card interactions"""
    rsp1 = Path(f'{cfg.datadir}plot_rs.pdf')
    rsp2 = Path(f'{cfg.datadir}plot_rs_testplot.pdf')
    pac = PlotAlgoCompare()
    pac_pfn = pac.build_plot_file_name()
    assert rsp1 == pac_pfn
    pac_pfn = pac.build_plot_file_name(plot_id="testplot")
    assert rsp2 == pac_pfn

def test_get_run_num(config_event_defaults):
    """test generate run stats"""
    miss_inter_cnt = 17
    pac = PlotAlgoCompare()
    cnt = pac.get_run_num("test_algo")
    assert cnt == 0
    cnt = pac.get_run_num("test_algo")
    assert cnt == 1
    cnt = pac.get_run_num("test_algo2")
    assert cnt == 0
