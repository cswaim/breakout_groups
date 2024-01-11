from collections import Counter

import datetime
from src.reports_run_stats import RunStats
from src import config as cfg
#from src import sessions_util as su
import pytest

"""Unit tests for run statistics"""

def test_build_all_card_interactions(config_event_defaults):
    """test building of all card interactions"""
    rsp = {0: [4, 1, 0, 2, 0, 2, 2, 1, 0, 2, 0],
           1: [1, 4, 2, 1, 1, 1, 0, 3, 0, 1, 0],
           2: [0, 2, 4, 0, 3, 1, 1, 1, 2, 0, 1],
           3: [2, 1, 0, 4, 0, 2, 1, 1, 0, 4, 1],
           4: [0, 1, 3, 0, 4, 1, 2, 0, 3, 0, 2],
           5: [2, 1, 1, 2, 1, 4, 1, 0, 0, 2, 1],
           6: [2, 0, 1, 1, 2, 1, 4, 0, 2, 1 ,1],
           7: [1, 3, 1, 1, 0, 0, 0, 4, 1, 1 ,1],
           8: [0, 0, 2, 0, 3, 0, 2, 1, 4, 0, 3],
           9: [2, 1, 0, 4, 0, 2, 1, 1, 0, 4, 1],
          10: [0, 0, 1, 1, 2, 1, 1, 1, 3, 1, 4],
          }
    # su_interactions = su.build_all_card_interactions()
    rrs = RunStats()
    rrs_interactions = rrs.build_interactions()
    #assert su_interactions == rrs_interactions
    assert rsp == rrs_interactions

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
    assert 60 == rrs.max_i
    assert 12 == rrs.max_idivi
    assert mcnt == rrs.miss_inter_cnt

