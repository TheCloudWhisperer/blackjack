#!/usr/local/bin/python

# Imports
from random import shuffle as sh
import bj_classes

# Global Variables:
# The "source deck" is the full, ordered deck of cards - this should never change,
# hence we define it as a tuple
source_deck = ('Ac', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc',
              'Ad', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd',
              'Ah', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh',
              'As', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks')
# The "playing deck" is the deck currently in use - it will be 'populated' with the
# cards from the "source deck" and then shuffled every time
playing_deck = []
# Not sure if I will need this - may use to keep track of the cards that have already
# been drawn from the deck in play
drawn_cards = []

"""
We will have to replenish and reshuffle the deck every time we start a new "game"
"""
def init_game_deck():
    global playing_deck
    playing_deck = list(source_deck)
    sh(playing_deck)

dealer = Participant()
player = Player()


# Debug

print player.cards

#playing_deck = list(source_deck)

# shuffling the deck
#sh(playing_deck)

playing_deck

init_game_deck()

#tmp_card = str(playing_deck.pop())
#print tmp_card
#type(tmp_card)
player.add_card(playing_deck.pop())
print player.cards
