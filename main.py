import random
import re
from itertools import combinations
import flet as ft

# Frame Knowledge Representation untuk Kartu
class Card:
    # Atribut dari Card
    suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
    values = {
        2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
        8: '8', 9: '9', 10: '10', 11: 'Jack', 
        12: 'Queen', 13: 'King', 14: 'Ace'
    }
    suit_map = {'s': 'Spades', 'h': 'Hearts', 'd': 'Diamonds', 'c': 'Clubs' }
    value_map = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10,
                 'J':11, 'Q':12, 'K':13, 'A':14}
    
    # Symbols for suits
    suit_symbols = {
        'Spades': '♠',
        'Hearts': '♥',
        'Diamonds': '♦',
        'Clubs': '♣'
    }
    
    # Colors for suits
    suit_colors = {
        'Spades': 'black',
        'Hearts': 'red',
        'Diamonds': 'red',
        'Clubs': 'black'
    }

    # Method Constructor
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.values[self.value]} of {self.suit}"
    
    @property
    def short_name(self):
        """Short name for the card (e.g., 'A♥')"""
        value_str = self.values[self.value]
        if value_str == '10':
            value_short = '10'
        else:
            value_short = value_str[0]
        return f"{value_short}{self.suit_symbols[self.suit]}"
    
    @property
    def color(self):
        """Return the color of the card"""
        return self.suit_colors[self.suit]

    @property
    def chip_value(self):   # Menghitung nilai chip berdasarkan aturan tertentu (Ace = 11, J/Q/K = 10)
        if self.value == 14:
            return 11
        elif self.value in [11, 12, 13]:
            return 10
        else:
            return self.value

    @classmethod
    def from_code(cls, code):   # Membuat objek kartu dari kode string (seperti 'Ah' untuk Ace of Hearts)
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

# Frame Knowledge Representation untuk game state
class BalatroPoker:
    COMBO_DEFINITIONS = [   # Rule untuk mendefinisikan combo
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

    def __init__(self, page: ft.Page = None):
        self.page = page
        self.game_state = {
            'hand': [],
            'played_cards': [],
            'discarded': [],
            'discard_count': 0,
            'required_points': 300,
            'current_points': 0,
            'round_number': 1,
            'deck': []
        }
        self.selected_indices = []
        self.combo_info = None
        self.notification = None

    def start_round(self):
        self.game_state = {
            'hand': [],
            'played_cards': [],
            'discarded': [],
            'discard_count': 0,
            'required_points': 300,
            'current_points': 0,
            'round_number': self.game_state.get('round_number', 1) + 1,
            'deck': self.initialize_deck()
        }
        self.selected_indices = []
        self.combo_info = None
        for _ in range(8):
            self.deal_card()
        self.update_ui()

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
            self.show_notification("Deck is empty! No more cards to deal.")

    def play_combo(self):
        if not self.selected_indices:
            self.show_notification("No cards selected to play!")
            return
        
        hand = self.game_state['hand']
        selected_cards = [hand[i] for i in self.selected_indices]
        
        # Identify the played combo
        combo_info = self.identify_combo(selected_cards)
        if not combo_info:
            self.show_notification("No valid combo recognized! No points awarded.")
            return
        
        # Remove cards from hand
        removed = []
        for i in sorted(self.selected_indices, reverse=True):
            removed.append(hand.pop(i))
        
        self.game_state['played_cards'].extend(removed)
        needed = 8 - len(hand)
        for _ in range(needed):
            self.deal_card()
            
        # Calculate and add score
        base = combo_info['score']['base']
        mult = combo_info['score']['mult']
        chip_sum = sum(c.chip_value for c in removed)
        score = (base + chip_sum) * mult
        self.game_state['current_points'] += score
        
        self.show_notification(f"Played {combo_info['name']} and earned {score} points!")
        self.selected_indices = []
        self.update_ui()

    def identify_combo(self, combo_cards):
        for combo_def in self.COMBO_DEFINITIONS:
            required_count = combo_def['card_count']
            if len(combo_cards) < required_count:
                continue
            check_func = combo_def['check']
            # Apply the check function to the first required_count cards
            if check_func(combo_cards[:required_count]):
                return {
                    'name': combo_def['name'],
                    'score': combo_def['score']
                }
        return {'name': 'High Card', 'score': {'base': 5, 'mult': 1}}

    def discard_cards(self):
        if not self.selected_indices:
            self.show_notification("No cards selected to discard!")
            return
        
        hand = self.game_state['hand']
        discarded = []
        
        # Sort descending to avoid index shifting issues
        for i in sorted(self.selected_indices, reverse=True):
            discarded.append(hand.pop(i))
            
        self.game_state['discarded'].extend(discarded)
        needed = 8 - len(hand)
        for _ in range(needed):
            self.deal_card()
            
        self.show_notification(f"Discarded {len(discarded)} cards.")
        self.selected_indices = []
        self.update_ui()

    def analyze_hand(self):
        hand = self.game_state['hand']
        if not hand:
            self.show_notification("No cards in hand to analyze.")
            return []

        all_combos = []
        # Evaluate each combo definition with its required card count
        for combo_def in self.COMBO_DEFINITIONS:
            required_count = combo_def['card_count']
            if required_count > len(hand):
                continue
            # Generate all combinations of required_count cards
            for combo in combinations(hand, required_count):
                # Check if this combination meets the combo_def's criteria
                if combo_def['check'](combo):
                    base = combo_def['score']['base']
                    mult = combo_def['score']['mult']
                    chip_sum = sum(c.chip_value for c in combo)
                    score = (base + chip_sum) * mult
                    all_combos.append({
                        'name': combo_def['name'],
                        'cards': combo,
                        'score': score
                    })

        # Add High Card combo
        high_card_combo = None
        if hand:
            max_card = max(hand, key=lambda c: c.value)
            chip_sum = max_card.chip_value
            score = (5 + chip_sum) * 1
            high_card_combo = {
                'name': 'High Card',
                'cards': (max_card,),
                'score': score
            }
            all_combos.append(high_card_combo)

        # Remove duplicate combinations and sort by score
        unique_combos = []
        seen = set()
        for combo in all_combos:
            # Use a frozenset of card object IDs to track duplicates
            cards_tuple = tuple(sorted(combo['cards'], key=lambda x: x.value))
            combo_key = (combo['name'], cards_tuple)
            if combo_key not in seen:
                seen.add(combo_key)
                unique_combos.append(combo)

        # Sort by score descending, then by name ascending
        unique_combos.sort(key=lambda x: (-x['score'], x['name']))
        
        return unique_combos

    def toggle_card_selection(self, index):
        if index in self.selected_indices:
            self.selected_indices.remove(index)
        else:
            self.selected_indices.append(index)
        self.update_ui()

    def show_notification(self, message):
        self.notification = message
        self.update_ui()

    def create_card_container(self, card, index):
        selected = index in self.selected_indices
        
        card_container = ft.Container(
            content=ft.Column([
                ft.Text(
                    card.short_name,
                    size=24,
                    weight="bold",
                    color=card.color
                ),
                ft.Text(
                    f"{card.values[card.value]}",
                    size=14,
                    color=card.color
                ),
                ft.Text(
                    f"of {card.suit}",
                    size=12,
                    color=card.color
                ),
                ft.Text(
                    f"Value: {card.chip_value}",
                    size=10
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            width=100,
            height=140,
            border_radius=10,
            border=ft.border.all(2, "blue" if selected else "gray"),
            bgcolor="#f0f0f0" if not selected else "#d0e0ff",
            padding=10,
            ink=True,
            on_click=lambda e, i=index: self.toggle_card_selection(i)
        )
        return card_container

    def build_combo_details(self):
        combos = self.analyze_hand()
        
        if not combos:
            return [ft.Text("No valid combos found.")]
        
        combo_list = []
        for i, combo in enumerate(combos[:5]):  # Show top 5 combos
            card_indices = []
            for card in combo['cards']:
                try:
                    idx = self.game_state['hand'].index(card)
                    card_indices.append(idx)
                except ValueError:
                    pass
                    
            combo_container = ft.Container(
                content=ft.Column([
                    ft.Text(f"{combo['name']}", weight="bold"),
                    ft.Text(f"Score: {combo['score']}"),
                    ft.Text(f"Cards: {', '.join(c.short_name for c in combo['cards'])}"),
                    ft.ElevatedButton(
                        text="Select Cards",
                        on_click=lambda e, indices=card_indices: self.select_combo_cards(indices)
                    )
                ]),
                bgcolor="#e8e8e8",
                padding=10,
                border_radius=5,
                margin=5
            )
            combo_list.append(combo_container)
            
        return combo_list
    
    def select_combo_cards(self, indices):
        self.selected_indices = indices
        self.update_ui()

    def update_ui(self):
        if not self.page:
            return
            
        # Build card display for hand
        hand_cards = []
        for i, card in enumerate(self.game_state['hand']):
            hand_cards.append(self.create_card_container(card, i))
            
        # Build card display for played and discarded cards
        played_cards_row = ft.Row([
            ft.Container(
                content=ft.Text(
                    f"{card.short_name}",
                    size=16,
                    color=card.color
                ),
                padding=5,
                margin=2,
                bgcolor="#e0e0e0",
                border_radius=5
            ) for card in self.game_state['played_cards'][-10:]  # Only show last 10
        ], wrap=True)
        
        discarded_cards_row = ft.Row([
            ft.Container(
                content=ft.Text(
                    f"{card.short_name}",
                    size=16,
                    color=card.color
                ),
                padding=5,
                margin=2,
                bgcolor="#e0e0e0",
                border_radius=5
            ) for card in self.game_state['discarded'][-10:]  # Only show last 10
        ], wrap=True)
        
        # Create combo list
        combo_details = self.build_combo_details()
        
        # Create notification display
        notification_display = ft.Text(
            self.notification if self.notification else "",
            color="green" if self.notification and "earned" in self.notification else "red",
            size=16,
            weight="bold"
        )
        
        # Update the page content
        self.page.controls = [
            ft.AppBar(
                title=ft.Text("Balatro Poker Assistant"),
                bgcolor=ft.colors.BLUE_700
            ),
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"Round: {self.game_state['round_number']}", weight="bold"),
                        ft.Text(f"Points: {self.game_state['current_points']} / {self.game_state['required_points']}", weight="bold"),
                        ft.Text(f"Deck: {len(self.game_state['deck'])} cards left", weight="bold")
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    
                    notification_display,
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Your Hand:", weight="bold", size=18),
                            ft.Row(hand_cards, wrap=True)
                        ]),
                        padding=10,
                        bgcolor="#f8f8f8",
                        border_radius=10,
                        margin=5
                    ),
                    
                    ft.Row([
                        ft.ElevatedButton(
                            "Play Combo",
                            icon=ft.icons.PLAY_ARROW,
                            on_click=lambda _: self.play_combo(),
                            disabled=len(self.selected_indices) == 0
                        ),
                        ft.ElevatedButton(
                            "Discard Cards",
                            icon=ft.icons.DELETE,
                            on_click=lambda _: self.discard_cards(),
                            disabled=len(self.selected_indices) == 0
                        ),
                        ft.ElevatedButton(
                            "Reset Round",
                            icon=ft.icons.REFRESH,
                            on_click=lambda _: self.start_round()
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    
                    ft.Tabs(
                        tabs=[
                            ft.Tab(
                                text="Analyze Hand",
                                content=ft.Container(
                                    content=ft.Column(combo_details),
                                    padding=10
                                )
                            ),
                            ft.Tab(
                                text="Played Cards",
                                content=ft.Container(
                                    content=ft.Column([
                                        ft.Text("Played Cards:", weight="bold"),
                                        played_cards_row
                                    ]),
                                    padding=10
                                )
                            ),
                            ft.Tab(
                                text="Discarded Cards",
                                content=ft.Container(
                                    content=ft.Column([
                                        ft.Text("Discarded Cards:", weight="bold"),
                                        discarded_cards_row
                                    ]),
                                    padding=10
                                )
                            ),
                            ft.Tab(
                                text="Combo Scores",
                                content=ft.Container(
                                    content=ft.Column([
                                        ft.Text("Combo Scores:", weight="bold"),
                                        ft.DataTable(
                                            columns=[
                                                ft.DataColumn(ft.Text("Combo")),
                                                ft.DataColumn(ft.Text("Base")),
                                                ft.DataColumn(ft.Text("Multiplier"))
                                            ],
                                            rows=[
                                                ft.DataRow(cells=[
                                                    ft.DataCell(ft.Text(combo['name'])),
                                                    ft.DataCell(ft.Text(str(combo['score']['base']))),
                                                    ft.DataCell(ft.Text(str(combo['score']['mult'])))
                                                ]) for combo in self.COMBO_DEFINITIONS
                                            ] + [
                                                ft.DataRow(cells=[
                                                    ft.DataCell(ft.Text("High Card")),
                                                    ft.DataCell(ft.Text("5")),
                                                    ft.DataCell(ft.Text("1"))
                                                ])
                                            ]
                                        )
                                    ]),
                                    padding=10
                                )
                            )
                        ],
                        expand=True
                    )
                ]),
                padding=20
            )
        ]
        
        self.page.update()

def main(page: ft.Page):
    page.title = "Balatro Poker Assistant"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Create the game instance
    game = BalatroPoker(page)
    
    # Set up the game
    game.start_round()
    
    # Display the UI
    page.update()

if __name__ == "__main__":
    ft.app(target=main)