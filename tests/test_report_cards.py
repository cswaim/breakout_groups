from collections import Counter

import os
from src import config as cfg
from src.reports_cards import CardsReports
import pytest

"""Unit tests for print cards."""

def test_card_print(config_event_defaults, tmp_path):
    """test cardpdf"""
    cr = CardsReports()
    card_cnt = 0
    for c in cfg.all_cards:
        card_cnt += 1
        cr.card_print(c)
    print('')
    assert card_cnt == cfg.n_attendees

def test_card_txt(config_event_defaults, create_folders):
    """test cardpdf"""
    #cfg.datadir = str(tcreatemp_path_factory)
    cr = CardsReports()
    card_cnt = 0
    with open(f'{cfg.datadir}cards.txt', 'w') as ctxt:
        for c in cfg.all_cards:
            card_cnt += 1
            cr.card_txt(ctxt, c)

    assert card_cnt == cfg.n_attendees

def test_card_pdf(config_event_defaults, create_folders):
    """test cardpdf"""
    #cfg.datadir = str(tcreatemp_path_factory)
    cr = CardsReports()
    card_cnt = 0
    cpdf = cr.card_pdf_canvas()
    for c in cfg.all_cards:
        card_cnt += 1
        cr.card_pdf(cpdf, c)
    cpdf.save()

    assert card_cnt == cfg.n_attendees
