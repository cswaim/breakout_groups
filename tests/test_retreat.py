from src.retreat import Retreat

def test_find_missing_persons(get_config, get_random_seed):
    assert True

def test_get_interactions(retreat_cards):
    retreat = Retreat()
    result = retreat.get_interactions(all_cards=retreat_cards)
    assert result
    for k in result.keys():
        print(f"\n{k}")
        print(f"   {result[k]}\n")