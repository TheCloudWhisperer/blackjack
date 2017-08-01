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
        self.bankroll = bankroll
        self.bet = 0
        self.cards = []
        self.total_points = 0
        self.has_blackjack = False

    def add_funds(amount):
        self.bankroll += amount

    def take_funds(amount):
        self.bankroll -= amount

    def place_bet(amount):
        self.bankroll -= amount
        self.bet += amount
