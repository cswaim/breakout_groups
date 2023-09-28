from collections import Counter

import datetime
from src.reports_run_stats import RunStats
#from src import sessions_util as su
import pytest

"""Unit tests for run statistics"""

# def test_build_all_card_interactions(config_event_defaults):
#     """test building of all card interactions"""
#     su_interactions = su.build_all_card_interactions()
#     rrs = RunStats()
#     rrs_interactions = rrs.build_interactions()
#     assert su_interactions == rrs_interactions

def test_gen_run_stats(config_event_defaults):
    """test generate run stats"""
    miss_inter_cnt = 17
    rrs = RunStats()
    rrs.gen_run_stats()
    mcnt = 0
    for k,v in rrs.all_interactions.items():
        mcnt += v.count(0)
    mcnt = mcnt // 2
    assert 38 == rrs.inter_cnt
    assert 16 == rrs.dup_inter_cnt
    assert 22 == rrs.unique_inter_cnt
    assert 55 == rrs.pui
    assert 44 == rrs.maxpui
    assert  8 == rrs.maxidivi
    assert mcnt == rrs.miss_inter_cnt


def test_gen_run_stats_orig(config_event_defaults):
    """test generate run stats"""
    miss_inter_cnt = 17
    rrs = RunStats()
    rrs.gen_run_stats_orig()
    mcnt = 0
    for k,v in rrs.all_interactions.items():
        mcnt += v.count(0)
    mcnt = mcnt // 2
    assert 38 == rrs.inter_cnt
    assert 16 == rrs.dup_inter_cnt
    assert 22 == rrs.unique_inter_cnt
    assert 55 == rrs.pui
    assert 44 == rrs.maxpui
    assert  8 == rrs.maxidivi
    assert mcnt == rrs.miss_inter_cnt
