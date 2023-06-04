from collections import Counter
from itertools import combinations
from src import config as cfg
from src.card import Card
import logging

log = logging.getLogger(__name__)

"""Utilities for sessions """


class SessionsUtils:
    """Create dict of interactions amon attendees"""

    def init_cards(nc=cfg.n_attendees) -> list:
        """ build the all_cards dict"""
        all_cards = []
        for i in range(nc):
            all_cards.append(Card(i))
        return all_cards

    def update_cards(all_cards) -> list:
        """ update individual card iteractions and labels"""
        # k is session num,ber v is group list
        for k, v in cfg.sessions.items():
            # update card with group info, n grp num and g is group list of attendees
            for n, g in enumerate(v):
                upd_dict = all_cards[0].convert_grp_to_dict(g)
                for c in g:
                    all_cards[c].update_cards(upd_dict)
                    # set the group label, if label not found, use default
                    try:
                        glabel = cfg.group_labels[k][n]
                    except:
                        glabel = f"group{n}"
                    all_cards[c].update_sess_labels(glabel)
        return all_cards

    def build_all_card_interactions():
        """build a list of all the interactions from all cards """
        all_card_interactions = {}
        for c in cfg.all_cards:
            all_card_interactions[c.id] = c.card_interactions

        return all_card_interactions
