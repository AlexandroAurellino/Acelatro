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
    
    pass