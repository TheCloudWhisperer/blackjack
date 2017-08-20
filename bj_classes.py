"""
We need a Player class, which we will use to keep track of cards for both dealer
and player.

We will also keep track of:
- player's bankroll
- player's cards in hand
"""

# "Participant" Class (could be either the Dealer or Player)
class Participant(object):

    def __init__(self):
        self.cards = []
        self.total_points = 0
        self.has_blackjack = False
    
    def add_card(self,card):
        self.cards.append(card)


# "Player" Class
class Player(Participant):

    def __init__(self,bankroll=0):
        self.name = ""
        self.bankroll = bankroll
        self.bet = 0
        self.cards = []
        self.total_points = 0
        self.has_blackjack = False
        self.has_insurance = False
        self.insurance = 0

    def add_funds(amount):
        self.bankroll += amount

    def take_funds(amount):
        self.bankroll -= amount

    def place_bet(amount):
        self.bankroll -= amount
        self.bet += amount


# The "source deck" is the full, ordered deck of cards - this should never change,
# hence we define it as a tuple
base_deck = ('Ac', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc',
             'Ad', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd',
             'Ah', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh',
             'As', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks')


# Let's also have a dictionary to translate short card notation into human notation
card_dict = {
    'Ac': 'Ace of Clubs',
    '2c': '2 of Clubs',
    '3c': '3 of Clubs',
    '4c': '4 of Clubs',
    '5c': '5 of Clubs',
    '6c': '6 of Clubs',
    '7c': '7 of Clubs',
    '8c': '8 of Clubs',
    '9c': '9 of Clubs',
    'Tc': '10 of Clubs',
    'Jc': 'Jack of Clubs',
    'Qc': 'Queen of Clubs',
    'Kc': 'King of Clubs',
    'Ad': 'Ace of Diamonds',
    '2d': '2 of Diamonds',
    '3d': '3 of Diamonds',
    '4d': '4 of Diamonds',
    '5d': '5 of Diamonds',
    '6d': '6 of Diamonds',
    '7d': '7 of Diamonds',
    '8d': '8 of Diamonds',
    '9d': '9 of Diamonds',
    'Td': '10 of Diamonds',
    'Jd': 'Jack of Diamonds',
    'Qd': 'Queen of Diamonds',
    'Kd': 'King of Diamonds',
    'Ah': 'Ace of Hearts',
    '2h': '2 of Hearts',
    '3h': '3 of Hearts',
    '4h': '4 of Hearts',
    '5h': '5 of Hearts',
    '6h': '6 of Hearts',
    '7h': '7 of Hearts',
    '8h': '8 of Hearts',
    '9h': '9 of Hearts',
    'Th': '10 of Hearts',
    'Jh': 'Jack of Hearts',
    'Qh': 'Queen of Hearts',
    'Kh': 'King of Hearts',
    'As': 'Ace of Spades',
    '2s': '2 of Spades',
    '3s': '3 of Spades',
    '4s': '4 of Spades',
    '5s': '5 of Spades',
    '6s': '6 of Spades',
    '7s': '7 of Spades',
    '8s': '8 of Spades',
    '9s': '9 of Spades',
    'Ts': '10 of Spades',
    'Js': 'Jack of Spades',
    'Qs': 'Queen of Spades',
    'Ks': 'King of Spades'
}