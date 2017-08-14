#!/usr/local/bin/python

# Imports
from random import shuffle as sh
import bj_classes as bjc

# Global Variables:
# The "source deck" is the full, ordered deck of cards - this should never change,
# hence we define it as a tuple
base_deck = ('Ac', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc',
             'Ad', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd',
             'Ah', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh',
             'As', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks')
# The "playing deck" is the deck currently in use - it will be 'populated' with the
# cards from the "source deck" and then shuffled every time
playing_deck = []
# Not sure if I will need this - may use to keep track of the cards that have already
# been drawn from the deck in play
drawn_cards = []
# Defining the Dealer and Player objects as global
dealer = bjc.Participant()
player = bjc.Player()

# ---- ---- ----

"""
Supporting functions
"""

"""
Setting up the player
"""
def ask_player_name():
    """
    This function will be called during the game's init phase to greet the
    Player and record their name.
    It will return the player's name as a string.

    ToDo: We could ask confirmation that the name entered is correct, and if not
    offer the player to reset their name - left for future improvement, keeping it
    simple for now.
    """

    valid_name = False

    print "\n\tHello Player!"

    while not valid_name:

        player_name = raw_input("\n\tWhat is your name? [Press Enter to confirm]: ")

        if player_name == '':
            print "\n\tI am sorry, I did not catch your name." \
                  "\n\tPlease try again.."
        else:
            valid_name = True

    return player_name


"""
Adding funds to the player's bankroll
"""
def add_money():

    global player
    valid_answer = False

    while not valid_answer:
        try:
            amount = int(raw_input("\n\tHow much money do you want to add to your pot? [Press Enter to confirm]: "))
        except ValueError as ex:
            print "\n\tI am afraid that is not a valid amount." \
                  "\n\tPlease try again!"
        else:
            print "\n\tThank you, I added that to your pot!"
            player.bankroll += amount
            valid_answer = True


"""
Take player bet.
Bet can only be integer numbers.
"""
def take_player_bet():

    global player
    valid_bet = False

    # Checking players' funds first: if Zero, then offer to add funds
    # (separate function?)

    print "\n\tHello %s!" % (player.name)

    if player.bankroll == 0:
        answer = raw_input("\n\tYou currently have no funds, would you like to add some? [y/N]: ")

        if answer == 'y':   # add other checks, like capital Y, etc...
            add_money()
        else:
            print "\n\tSince you have no funds and no intention to add any, your game ends here!" \
                  "\n\tThank you for playing %s!\n" % (player.name)
            exit(100)

    while not valid_bet:
        # Asking the player to bet
        try:
            bet = int(raw_input("\n\tPlease, place your bet! [Press Enter to confirm]: "))
        except ValueError as ex:
            print "\n\tI am afraid that was not a valid bet." \
                  "\n\tPlease try again!"
        else:
            if bet > player.bankroll:
                print "\n\tI am afraid do not have sufficient funds." \
                      "\n\tYou currently have %s at your disposal." \
                      "\n\tPlease try again!" % (player.bankroll)
            else:
                valid_bet = True

    return bet


"""
We will have to replenish and reshuffle the deck every time we start a new "game"
"""
def init_game_deck():
    """
    We set the contents of the global variable that is the playing deck by
    transforming the base deck (tuple) into a list that we can "pop" cards out
    of.
    We then shuffle the playing deck, so that cards are always popped from the
    end of the list, but are also randomised.
    """
    global playing_deck

    playing_deck = list(base_deck)

    sh(playing_deck)


# Debug

#print player.cards

#playing_deck = list(base_deck)

# shuffling the deck
#sh(playing_deck)

#print playing_deck

#init_game_deck()

#tmp_card = str(playing_deck.pop())
#print tmp_card
#type(tmp_card)
#player.add_card(playing_deck.pop())
#print player.cards

# ---- ---- ----

"""
Main game functions
"""

def init_game():

    global player

    player.name = ask_player_name()
    print player.name


def play_game():

    # 1. Player bet
    print take_player_bet()

    # 2. 1 card to player, 1 card to dealer (both face up)

    # 3. 2nd card to player (face up), 2nd card to dealer (face down, unless bj)

    pass


def main():

    play_game()

# ---- ---- ----

"""
Script execution
"""

init_game()

main()