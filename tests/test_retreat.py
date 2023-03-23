from src.retreat import Retreat

def test_find_missing_persons(get_config, get_random_seed):
    assert True

def test_get_interactions(retreat_cards):
    retreat = Retreat()
    result = retreat.get_interactions(all_cards=retreat_cards)
    assert result

def test_show_interactions_by_persons(retreat_cards):
    retreat = Retreat()
    result = retreat.show_interactions_by_persons(all_cards=retreat_cards)
    assert result is None
