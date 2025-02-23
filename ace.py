import random
import re
from itertools import combinations

class Card:
    suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
    values = {
        2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
        8: '8', 9: '9', 10: '10', 11: 'Jack', 
        12: 'Queen', 13: 'King', 14: 'Ace'
    }
    suit_map = {'s': 'Spades', 'h': 'Hearts', 'd': 'Diamonds', 'c': 'Clubs'}
    value_map = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10,
                 'J':11, 'Q':12, 'K':13, 'A':14}

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.values[self.value]} of {self.suit}"

    @property
    def chip_value(self):
        if self.value == 14:
            return 11
        elif self.value in [11, 12, 13]:
            return 10
        else:
            return self.value

    @classmethod
    def from_code(cls, code):
        code = code.strip().upper().replace(' ', '')
        if len(code) < 2:
            return None
        suit_part = code[-1].lower()
        value_part = code[:-1]
        if suit_part not in cls.suit_map:
            return None
        suit = cls.suit_map[suit_part]
        if value_part.isdigit():
            value = int(value_part)
        else:
            value = cls.value_map.get(value_part)
        if not value or not (2 <= value <= 14):
            return None
        return cls(suit, value)

def is_royal_flush(cards):
    if len(cards) !=5:
        return False
    values = sorted([c.value for c in cards])
    return (values == [10, 11, 12, 13, 14] and
            is_flush(cards) and is_straight(cards))

def is_straight_flush(cards):
    return is_flush(cards) and is_straight(cards)

def is_flush(cards):
    return all(c.suit == cards[0].suit for c in cards)

def is_straight(cards):
    values = sorted([c.value for c in cards])
    return (values[-1] - values[0] ==4) and (len(set(values)) ==5)

def is_four_of_a_kind(cards):
    counts = {}
    for c in cards:
        counts[c.value] = counts.get(c.value, 0) +1
    return any(v >=4 for v in counts.values())

def is_full_house(cards):
    counts = {}
    for c in cards:
        counts[c.value] = counts.get(c.value, 0) +1
    return (2 in counts.values()) and (3 in counts.values())

def is_three_of_a_kind(cards):
    counts = {}
    for c in cards:
        counts[c.value] = counts.get(c.value, 0) +1
    return any(v >=3 for v in counts.values())

def is_two_pair(cards):
    counts = {}
    for c in cards:
        counts[c.value] = counts.get(c.value, 0) +1
    pairs = [k for k, v in counts.items() if v >=2]
    return len(pairs) >=2

def is_pair(cards):
    return len(cards) == 2 and cards[0].value == cards[1].value

class BalatroPoker:
    COMBO_DEFINITIONS = [
        {
            'name': 'Royal Flush',
            'card_count': 5,
            'check': is_royal_flush,
            'score': {'base': 100, 'mult': 8}
        },
        {
            'name': 'Straight Flush',
            'card_count': 5,
            'check': is_straight_flush,
            'score': {'base': 100, 'mult': 8}
        },
        {
            'name': 'Four of a Kind',
            'card_count': 4,
            'check': is_four_of_a_kind,
            'score': {'base': 60, 'mult': 7}
        },
        {
            'name': 'Full House',
            'card_count': 5,
            'check': is_full_house,
            'score': {'base': 40, 'mult': 4}
        },
        {
            'name': 'Flush',
            'card_count': 5,
            'check': is_flush,
            'score': {'base': 35, 'mult': 4}
        },
        {
            'name': 'Straight',
            'card_count': 5,
            'check': is_straight,
            'score': {'base': 30, 'mult': 4}
        },
        {
            'name': 'Three of a Kind',
            'card_count': 3,
            'check': is_three_of_a_kind,
            'score': {'base': 30, 'mult': 3}
        },
        {
            'name': 'Two Pair',
            'card_count': 4,
            'check': is_two_pair,
            'score': {'base': 20, 'mult': 2}
        },
        {
            'name': 'Pair',
            'card_count': 2,
            'check': is_pair,
            'score': {'base': 10, 'mult': 2}
        }
    ]

    def __init__(self):
        self.game_state = {
            'hand': [],
            'played_cards': [],
            'discarded': [],
            'discard_count': 0,
            'required_points': 1000,
            'current_points': 0,
            'round_number': 1,
            'deck': []
        }

    def start_round(self):
        self.game_state = {
            'hand': [],
            'played_cards': [],
            'discarded': [],
            'discard_count': 0,
            'required_points': 1000,
            'current_points': 0,
            'round_number': self.game_state.get('round_number', 1) + 1,
            'deck': self.initialize_deck()
        }
        for _ in range(8):
            self.deal_card()

    def initialize_deck(self):
        deck = []
        for suit in Card.suits:
            for value in range(2, 15):
                deck.append(Card(suit, value))
        random.shuffle(deck)
        return deck

    def deal_card(self):
        if self.game_state['deck']:
            card = self.game_state['deck'].pop()
            self.game_state['hand'].append(card)
        else:
            print("Deck is empty! No more cards to deal.")

    def play_combo(self, combo_cards):
        removed = []
        hand = self.game_state['hand']
        combo_cards = [c for c in hand if c in combo_cards]
        for card in combo_cards:
            hand.remove(card)
            removed.append(card)
        if not removed:
            print("No cards selected to play!")
            return
        self.game_state['played_cards'].extend(removed)
        needed = 8 - len(hand)
        for _ in range(needed):
            self.deal_card()
        combo_info = self.identify_combo(removed)
        if combo_info:
            base = combo_info['score']['base']
            mult = combo_info['score']['mult']
            chip_sum = sum(c.chip_value for c in removed)
            score = (base + chip_sum) * mult
            self.game_state['current_points'] += score
            print(f"Played {combo_info['name']} and earned {score} points!")
        else:
            print("No combo recognized! No points awarded.")

    def identify_combo(self, combo_cards):
        for combo_def in self.COMBO_DEFINITIONS:
            required_count = combo_def['card_count']
            check_func = combo_def['check']
            base = combo_def['score']['base']
            mult = combo_def['score']['mult']
            if len(combo_cards) < required_count:
                continue
            # Check if any combination of required_count cards meets the condition
            # For simplicity, assume the entire combo_cards is checked
            if check_func(combo_cards[:required_count]):
                return {
                    'name': combo_def['name'],
                    'score': {'base': base, 'mult': mult}
                }
        return {'name': 'High Card', 'score': {'base':5, 'mult':1}}

    def discard_cards(self, indices):
        hand = self.game_state['hand']
        discarded = []
        valid_indices = []
        for idx in indices:
            if 0 <= idx < len(hand):
                valid_indices.append(idx)
        for idx in valid_indices:
            discarded.append(hand.pop(idx))
        self.game_state['discarded'].extend(discarded)
        needed = 8 - len(hand)
        for _ in range(needed):
            self.deal_card()
        print(f"Discarded {len(discarded)} cards.")

    def check_hand(self):
        print("\nYour Hand:")
        for idx, card in enumerate(self.game_state['hand']):
            print(f"{idx+1}: {card}")

    def check_discarded(self):
        print("\nDiscarded Cards:")
        for card in self.game_state['discarded']:
            print(card)

    def check_played(self):
        print("\nPlayed Cards:")
        for card in self.game_state['played_cards']:
            print(card)

    def analyze_hand(self):
        hand = self.game_state['hand']
        combos = []
        for combo_def in self.COMBO_DEFINITIONS:
            required_count = combo_def['card_count']
            check_func = combo_def['check']
            base = combo_def['score']['base']
            mult = combo_def['score']['mult']
            for combo_cards in combinations(hand, required_count):
                if check_func(combo_cards):
                    chip_sum = sum(c.chip_value for c in combo_cards)
                    total_score = (base + chip_sum) * mult
                    combos.append({
                        'name': combo_def['name'],
                        'cards': combo_cards,
                        'score': total_score
                    })
        # Add High Card combo
        if hand:
            max_card = max(hand, key=lambda c: c.value)
            chip_sum = max_card.chip_value
            total_score = (5 + chip_sum) * 1
            combos.append({
                'name': 'High Card',
                'cards': [max_card],
                'score': total_score
            })
        if combos:
            best_combo = max(combos, key=lambda x: x['score'])
            print(f"Recommended combo: {best_combo['name']}")
            print("Recommended cards to play:")
            for idx, card in enumerate(best_combo['cards']):
                print(f"{idx+1}: {card}")
            # Find indices in hand
            indices = []
            for card in best_combo['cards']:
                try:
                    idx = self.game_state['hand'].index(card)
                    indices.append(idx + 1)  # 1-based index
                except ValueError:
                    pass
            print("Suggested indices:", ", ".join(map(str, indices)))
        else:
            print("No valid combos found.")

    def show_combo_scores(self):
        print("\nCombo Scores:")
        for combo_def in self.COMBO_DEFINITIONS:
            print(f"{combo_def['name']}: {combo_def['score']['base']} chips x {combo_def['score']['mult']} multiplier")
        print("High Card: 5 chips x 1 multiplier")

    def reset_round(self):
        self.start_round()
        print("Round reset!")

    def main_loop(self):
        print("Welcome to Balatro Poker Assistant!")
        self.start_round() 
        while True:
            print("\nCurrent Points:", self.game_state['current_points'])
            print("Required Points:", self.game_state['required_points'])
            print("\nMain Menu:")
            print("1. Check current hand")
            print("2. Play combo (select cards)")
            print("3. Discard cards (select indices)")
            print("4. Check discarded cards")
            print("5. Check played cards")
            print("6. Analyze hand for combos")
            print("7. Show combo scores")
            print("8. Reset round")
            print("9. Quit")
            choice = input("Enter your choice (1-9): ").strip()

            if choice == '1':
                self.check_hand()
            elif choice == '2':
                self.check_hand()
                selected = input("Enter indices of cards to play (e.g., '1 3 5'): ")
                indices = [int(i)-1 for i in selected.split()]
                combo_cards = [self.game_state['hand'][i] for i in indices if 0 <= i < len(self.game_state['hand'])]
                self.play_combo(combo_cards)
            elif choice == '3':
                self.check_hand()
                selected = input("Enter indices of cards to discard (e.g., '1 3 5'): ")
                indices = [int(i)-1 for i in selected.split()]
                self.discard_cards(indices)
            elif choice == '4':
                self.check_discarded()
            elif choice == '5':
                self.check_played()
            elif choice == '6':
                self.analyze_hand()
            elif choice == '7':
                self.show_combo_scores()
            elif choice == '8':
                self.reset_round()
            elif choice == '9':
                print("Exiting Balatro Poker Assistant. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    game = BalatroPoker()
    game.main_loop()