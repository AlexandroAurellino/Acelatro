# Rules untuk menentukan combo
def is_royal_flush(cards):
    if len(cards) != 5:
        return False
    values = sorted([c.value for c in cards])
    return values == [10, 11, 12, 13, 14] and is_flush(cards) and is_straight(cards)

def is_straight_flush(cards):
    return is_flush(cards) and is_straight(cards)

def is_flush(cards):
    return all(c.suit == cards[0].suit for c in cards)

def is_straight(cards):
    values = sorted([c.value for c in cards])
    return (values[-1] - values[0] == 4) and (len(set(values)) == 5)

def is_four_of_a_kind(cards):
    counts = {}
    for c in cards:
        counts[c.value] = counts.get(c.value, 0) + 1
    return any(v == 4 for v in counts.values())

def is_full_house(cards):
    counts = {}
    for c in cards:
        counts[c.value] = counts.get(c.value, 0) + 1
    return sorted(counts.values()) == [2, 3]

def is_three_of_a_kind(cards):
    counts = {}
    for c in cards:
        counts[c.value] = counts.get(c.value, 0) + 1
    return any(v == 3 for v in counts.values())

def is_two_pair(cards):
    counts = {}
    for c in cards:
        counts[c.value] = counts.get(c.value, 0) + 1
    pairs = [k for k, v in counts.items() if v >= 2]
    return len(pairs) >= 2

def is_pair(cards):
    return len(cards) == 2 and cards[0].value == cards[1].value

pass