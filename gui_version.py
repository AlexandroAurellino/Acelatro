import tkinter as tk
import random
from itertools import combinations

class Card:
    suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
    values = {
        2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
        8: '8', 9: '9', 10: '10', 11: 'Jack', 
        12: 'Queen', 13: 'King', 14: 'Ace'
    }
    suit_abbr = {'Spades': 's', 'Hearts': 'h', 'Diamonds': 'd', 'Clubs': 'c'}
    suit_map = {'s': 'Spades', 'h': 'Hearts', 'd': 'Diamonds', 'c': 'Clubs' }
    value_map = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10,
                 'J':11, 'Q':12, 'K':13, 'A':14}

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.values[self.value]} of {self.suit}"

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.suit == other.suit and self.value == other.value
        return False

    def __hash__(self):
        return hash((self.suit, self.value))

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
    
    def gui_string(self):
        value_abbr = self.values[self.value][0] if self.value != 10 else 'T'
        return f"{value_abbr}{self.suit_abbr[self.suit]}".upper()

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
    return any(v ==4 for v in counts.values())

def is_full_house(cards):
    counts = {}
    for c in cards:
        counts[c.value] = counts.get(c.value, 0) +1
    return sorted(counts.values()) == [2, 3]

def is_three_of_a_kind(cards):
    counts = {}
    for c in cards:
        counts[c.value] = counts.get(c.value, 0) +1
    return any(v ==3 for v in counts.values())

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
            'plays_remaining': 3,
            'required_points': 300,
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
            'plays_remaining': 3,
            'required_points': 300,
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
        valid_combo = []
        for card in combo_cards:
            for h_card in hand:
                if h_card == card:
                    valid_combo.append(h_card)
                    break
        for card in valid_combo:
            hand.remove(card)
            removed.append(card)
        self.game_state['played_cards'].extend(removed)
        needed = 8 - len(hand)
        for _ in range(needed):
            self.deal_card()
        combo_info = self.identify_combo(removed)
        self.game_state['plays_remaining'] -= 1
        return combo_info

    def identify_combo(self, combo_cards):
        for combo_def in self.COMBO_DEFINITIONS:
            required_count = combo_def['card_count']
            if len(combo_cards) < required_count:
                continue
            check_func = combo_def['check']
            if check_func(combo_cards[:required_count]):
                return {
                    'name': combo_def['name'],
                    'score': combo_def['score']
                }
        return {'name': 'High Card', 'score': {'base':5, 'mult':1}}

    def discard_cards(self, indices):
        if self.game_state['discard_count'] >= 5:
            return False  # Cannot discard more than 5 times per round
        hand = self.game_state['hand']
        discarded = []
        indices = sorted(list(set(indices)), reverse=True)
        for idx in indices:
            if 0 <= idx < len(hand):
                discarded.append(hand.pop(idx))
        self.game_state['discarded'].extend(discarded)
        self.game_state['discard_count'] += 1
        needed = 8 - len(hand)
        for _ in range(needed):
            self.deal_card()
        return True

    def check_hand(self):
        return self.game_state['hand']

    def check_played(self):
        return self.game_state['played_cards']

    def check_discarded(self):
        return self.game_state['discarded']

    def analyze_hand(self):
        hand = self.game_state['hand']
        if not hand:
            return {
                'recommendation': None,
                'combo_list': []
            }

        all_combos = []
        for combo_def in self.COMBO_DEFINITIONS:
            required_count = combo_def['card_count']
            if required_count > len(hand):
                continue
            for combo in combinations(hand, required_count):
                if combo_def['check'](combo):
                    base = combo_def['score']['base']
                    mult = combo_def['score']['mult']
                    chip_sum = sum(c.chip_value for c in combo)
                    score_total = (base + chip_sum) * mult
                    all_combos.append({
                        'name': combo_def['name'],
                        'cards': combo,
                        'score_total': score_total,
                        'base': base,
                        'mult': mult
                    })

        # High Card logic
        if hand:
            max_card = max(hand, key=lambda c: c.value)
            chip_sum = max_card.chip_value
            score_total = (5 + chip_sum) * 1
            high_card_combo = {
                'name': 'High Card',
                'cards': [max_card],
                'score_total': score_total,
                'base': 5,
                'mult': 1
            }
            all_combos.append(high_card_combo)

        unique_combos = []
        seen = set()
        for combo in all_combos:
            cards_tuple = tuple(sorted(combo['cards'], key=lambda x: x.value))
            combo_key = (combo['name'], cards_tuple)
            if combo_key not in seen:
                seen.add(combo_key)
                unique_combos.append(combo)

        unique_combos.sort(key=lambda x: (-x['score_total'], x['name']))

        combo_list = []
        for combo in unique_combos:
            combo_list.append({
                'name': combo['name'],
                'score_total': combo['score_total'],
                'base': combo['base'],
                'mult': combo['mult'],
                'cards': [c.gui_string() for c in combo['cards']]
            })

        recommendation = None
        if unique_combos:
            best_combo = unique_combos[0]
            recommendation = {
                'combo_name': best_combo['name'],
                'score_total': best_combo['score_total'],
                'base': best_combo['base'],
                'mult': best_combo['mult'],
                'cards': [c.gui_string() for c in best_combo['cards']]
            }

        return {
            'recommendation': recommendation,
            'combo_list': combo_list
        }

class PokerGUI:
    def __init__(self, master, poker_game):
        self.master = master
        self.master.title("Acelatro Poker Assistant")
        self.master.geometry("1000x600")
        self.master.resizable(False, False)
        self.poker_game = poker_game

        # Main container
        self.main_frame = tk.Frame(self.master, bg="#111315")
        self.main_frame.pack(fill="both", expand=True)

        # Configure grid layout
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=5)
        self.main_frame.grid_columnconfigure(2, weight=3)
        self.main_frame.grid_rowconfigure(0, weight=5)
        self.main_frame.grid_rowconfigure(1, weight=3)

        # Left panel (commands and stats)
        self.command_frame = tk.Frame(self.main_frame, bg="#2A2C2E")
        self.command_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # Middle panel (hand)
        self.hand_frame = tk.Frame(self.main_frame, bg="#111315")
        self.hand_frame.grid(row=0, column=1, sticky="nsew")

        # Right panel (cards available)
        self.cards_available_frame = tk.Frame(self.main_frame, bg="#2A2C2E")
        self.cards_available_frame.grid(row=0, column=2, sticky="nsew")

        # Bottom panel (combo analysis)
        self.combo_analysis_frame = tk.Frame(self.main_frame, bg="#2A2C2E")
        self.combo_analysis_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

        # Command buttons
        self.show_recommendation_button = tk.Button(self.command_frame, text="Show Recommendation", command=self.show_recommendation, bg="#DBB1E4", fg="white", font=("Arial", 12))
        self.show_recommendation_button.pack(fill="x", pady=5)

        self.play_combo_button = tk.Button(self.command_frame, text="Play Combo", command=self.play_combo, bg="#74D1B2", fg="white", font=("Arial", 12))
        self.play_combo_button.pack(fill="x", pady=5)

        self.reset_button = tk.Button(self.command_frame, text="Reset Round", command=self.reset_round, bg="#6DA3DA", fg="white", font=("Arial", 12))
        self.reset_button.pack(fill="x", pady=5)

        self.discard_button = tk.Button(self.command_frame, text="Discard Cards", command=self.discard_cards, bg="#C6D481", fg="white", font=("Arial", 12))
        self.discard_button.pack(fill="x", pady=5)

        # Stats panel
        self.stats_frame = tk.Frame(self.command_frame, bg="#2A2C2E")
        self.stats_frame.pack(fill="y", expand=True)

        self.point_label = tk.Label(self.stats_frame, text="Point: 0", fg="white", bg="#2A2C2E", font=("Arial", 12))
        self.point_label.pack(fill="x")

        self.plays_label = tk.Label(self.stats_frame, text="Plays Remaining: 3", fg="white", bg="#2A2C2E", font=("Arial", 12))
        self.plays_label.pack(fill="x")

        self.discard_label = tk.Label(self.stats_frame, text="Discard: 0", fg="white", bg="#2A2C2E", font=("Arial", 12))
        self.discard_label.pack(fill="x")

        # Hand display
        self.hand_canvas = tk.Canvas(self.hand_frame, bg="#111315")
        self.hand_canvas.pack(fill="both", expand=True)

        # Cards available display
        self.update_cards_available()

        # Combo analysis display
        self.combo_analysis_label = tk.Label(self.combo_analysis_frame, text="Combo Analysis: Loading...", fg="white", bg="#2A2C2E", font=("Arial", 14), justify="left")
        self.combo_analysis_label.pack(padx=20, pady=20)

        self.update_hand_display()
        self.update_combo_display()

    def show_recommendation(self):
        analysis_result = self.poker_game.analyze_hand()
        recommendation = analysis_result['recommendation']
        combo_list = analysis_result['combo_list']

        combo_text = "Recommended Combo:\n"
        if recommendation:
            combo_text += f"{recommendation['combo_name']}\n"
            combo_text += f"Score: Base {recommendation['base']} | Mult: x{recommendation['mult']} | Total: {recommendation['score_total']}\n"
            combo_text += f"Cards: {', '.join(recommendation['cards'])}\n"
        else:
            combo_text += "No valid combo found. Consider discarding.\n"

        combo_text += "\nAvailable Combos:\n"
        for combo in combo_list:
            combo_text += f"{combo['name']}: Base {combo['base']} | Mult: x{combo['mult']} | Total: {combo['score_total']}\n"
            combo_text += f"Cards: {', '.join(combo['cards'])}\n"

        self.combo_analysis_label.config(text=combo_text)

    def update_hand_display(self):
        for widget in self.hand_canvas.winfo_children():
            widget.destroy()

        hand = self.poker_game.game_state['hand']
        self.card_selected = []
        self.card_buttons = []

        # Create a frame to hold the card buttons
        card_frame = tk.Frame(self.hand_canvas, bg="#111315")
        card_frame.pack(fill="x", expand=True)

        for i, card in enumerate(hand):
            suit_color = self.get_suit_color(card.suit)
            var = tk.BooleanVar(value=False)
            btn = tk.Checkbutton(
                card_frame,
                text=card.gui_string(),
                variable=var,
                indicatoron=False,
                selectcolor="#C6D481",
                bg=suit_color,
                fg="white",
                font=("Arial", 14),
                command=lambda i=i: self.toggle_card_selection(i),
                width=4,
                height=2
            )
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            self.card_selected.append(var)
            self.card_buttons.append(btn)

        # Configure grid columns for even spacing
        for i in range(len(hand)):
            card_frame.grid_columnconfigure(i, weight=1, uniform="cards")

    def get_suit_color(self, suit):
        suit_colors = {
            'Spades': '#DBB1E4',
            'Hearts': '#74D1B2',
            'Clubs': '#6DA3DA',
            'Diamonds': '#C6D481'
        }
        return suit_colors.get(suit, '#2A2C2E')

    def toggle_card_selection(self, index):
        if self.card_selected[index].get():
            self.card_buttons[index].config(relief="sunken")
        else:
            self.card_buttons[index].config(relief="raised")

    def play_combo(self):
        selected = []
        for i, var in enumerate(self.card_selected):
            if var.get():
                selected.append(i)
        if not selected:
            self.combo_analysis_label.config(text="No cards selected.")
            return
        combo_cards = [self.poker_game.game_state['hand'][i] for i in selected]
        combo_info = self.poker_game.play_combo(combo_cards)
        if combo_info:
            self.update_hand_display()
            self.update_combo_display()
            self.update_plays_remaining()
            self.combo_analysis_label.config(text=f"Played {combo_info['name']} and earned points!")
        else:
            self.combo_analysis_label.config(text="Invalid combo.")

    def discard_cards(self):
        selected = []
        for i, var in enumerate(self.card_selected):
            if var.get():
                selected.append(i)
        if len(selected) > 5:
            self.combo_analysis_label.config(text="Cannot discard more than 5 cards at once.")
            return
        if self.poker_game.game_state['discard_count'] >= 5:
            self.combo_analysis_label.config(text="Cannot discard more than 5 times per round.")
            return
        success = self.poker_game.discard_cards(selected)
        if success:
            self.update_hand_display()
            self.update_combo_display()
            self.update_plays_remaining()
            self.combo_analysis_label.config(text="Cards discarded successfully.")
        else:
            self.combo_analysis_label.config(text="Discard failed.")

    def update_combo_display(self):
        analysis_result = self.poker_game.analyze_hand()
        combo_list = analysis_result['combo_list']
        combo_text = "Available Combos:\n"
        for combo in combo_list:
            combo_text += f"{combo['name']}: Base {combo['base']} | Mult: x{combo['mult']} | Total: {combo['score_total']}\n"
            combo_text += f"Cards: {', '.join(combo['cards'])}\n"
        self.combo_analysis_label.config(text=combo_text)

    def update_cards_available(self):
        for widget in self.cards_available_frame.winfo_children():
            widget.destroy()

        suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
        suit_colors = {
            'Spades': '#DBB1E4',
            'Hearts': '#74D1B2',
            'Clubs': '#6DA3DA',
            'Diamonds': '#C6D481'
        }

        for suit in suits:
            color = suit_colors[suit]
            frame = tk.Frame(self.cards_available_frame, bg=color)
            frame.pack(fill="x", pady=5)

            label = tk.Label(frame, text=f"{suit}:", fg="white", bg=color, font=("Arial", 12))
            label.pack(side="left", padx=5)

            remaining = [c.gui_string() for c in self.poker_game.game_state['deck'] if c.suit == suit]
            cards_label = tk.Label(frame, text=" ".join(remaining), fg="white", bg=color, font=("Arial", 10))
            cards_label.pack(side="left", padx=5)

    def update_plays_remaining(self):
        plays = self.poker_game.game_state['plays_remaining']
        self.plays_label.config(text=f"Plays Remaining: {plays}")

    def reset_round(self):
        self.poker_game.reset_round()
        self.update_hand_display()
        self.update_combo_display()
        self.update_cards_available()
        self.update_plays_remaining()
        self.combo_analysis_label.config(text="Round reset.")

# Initialize and run
if __name__ == "__main__":
    root = tk.Tk()
    game = BalatroPoker()
    game.start_round()
    app = PokerGUI(root, game)
    app.update_cards_available()
    root.mainloop()