import random

def group_items(items, subset_size, num_rounds):
    subsets = []
    for i in range(num_rounds):
        # Randomly divide items into subsets for the first round
        if i == 0:
            random.shuffle(items)
            subsets = [items[j:j+subset_size] for j in range(0, len(items), subset_size)]
        else:
            used_subsets = []
            subsets = []
            for item in items:
                # Determine which subsets the item has been assigned to in previous rounds
                item_subsets = [subset for subset in used_subsets if item in subset]
                if len(item_subsets) == i:
                    # All subsets for this item have been used, so skip it for this round
                    continue
                # Identify the subsets that have the fewest items from previous rounds
                available_subsets = [subset for subset in subsets if subset not in item_subsets]
                fewest_items = min(len(subset) for subset in available_subsets)
                target_subsets = [subset for subset in available_subsets if len(subset) == fewest_items]
                # Randomly assign the item to one of the target subsets that it has not been assigned to before
                chosen_subset = random.choice([subset for subset in target_subsets if item not in subset])
                chosen_subset.append(item)
                used_subsets.append(chosen_subset)
                subsets.append(chosen_subset)
    return subsets