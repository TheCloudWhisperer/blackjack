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
#def add_money():
def add_money(entity):

    valid_answer = False

    while not valid_answer:
        try:
            amount = int(raw_input("\n\tHow much money do you want to add to your pot? [Press Enter to confirm]: "))
        except ValueError as ex:
            print "\n\tI am afraid that is not a valid amount." \
                  "\n\tPlease try again!"
        else:
            print "\n\tThank you, I added that to your pot!"
            entity.bankroll += amount
            valid_answer = True


"""
Taking funds from the player's bankroll
"""
def take_money(entity, amount):

    valid_answer = False

    while not valid_answer:

        if amount > entity.bankroll:
            print "Something has gone wrong, trying to bet more than you have in your pot."
            exit (200)

        else:
            entity.bankroll -= amount

            print "\n\tI have now taken %s out of your money pot." \
                  "\n\tYour remaining pot is: %s" % (str(amount),str(entity.bankroll))

            valid_answer = True


"""
Setting up initial player bankroll
"""
def bankroll_setup(entity):

    print "\n\tHello %s!\n\tLet's set up your money pot to start with..." % (entity.name)
    add_money(entity)


"""
Take player bet.
Bet can only be integer numbers.
"""
def take_player_bet(entity):

    #global player
    valid_bet = False

    # Checking players' funds first: if Zero, then offer to add funds
    # (separate function?)

    print "\n\tHello %s!" % (entity.name)

    if entity.bankroll == 0:
        answer = raw_input("\n\tYou currently have no funds, would you like to add some? [y/N]: ")

        if answer.lower() in ('y', 'yes'):   # add other checks, like capital Y, etc...
            #add_money()
            add_money(entity)
        else:
            print "\n\tSince you have no funds and no intention to add any, your game ends here!" \
                  "\n\tThank you for playing %s!\n" % (entity.name)
            exit(100)

    while not valid_bet:
        # Asking the player to bet
        try:
            bet = int(raw_input("\n\tPlease, place your bet! [Press Enter to confirm]: "))
        except ValueError as ex:
            print "\n\tI am afraid that was not a valid bet." \
                  "\n\tPlease try again!"
        else:
            if bet > entity.bankroll:
                print "\n\tI am afraid do not have sufficient funds." \
                      "\n\tYou currently have %s at your disposal." \
                      "\n\tPlease try again!" % (entity.bankroll)
            else:
                take_money(entity,bet)
                #We record the player's bet, so that we can calculate their wins
                entity.bet = bet
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


"""
Let's have a nice new function to assign cards to a player
"""
def give_card():

    global playing_deck

    card = playing_deck.pop()

    return card


"""
Need a function to check whether player/dealer has blackjack
"""
def has_blackjack(entity):

    """
    Either player will require a combination of Ace + ten points' card to have
    blackjack, seeds won't matter!
    Also, either will need exactly 2 cards.
    """
    has_ace = False
    has_ten = False

    if len(entity.cards) != 2:
        print "Wrong number of cards for blackjack."
        return False
    else:
        for card in entity.cards:
            if card[0] == 'A':
                has_ace = True
            elif card[0] in ['T', 'J', 'Q', 'K']:
                has_ten = True

    if has_ace and has_ten:
        return True
    else:
        return False



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
    # Debug
    print "\t" + player.name

    # Let's add some funds
    bankroll_setup(player)
    # Debug
    print "\tYour money pot currently is: " + str(player.bankroll)


def play_game():

    global player
    global dealer

    # 1. Shuffling the cards
    init_game_deck()

    # 2. Player bet - print only for Debug purposes
    print "\tYour bet: " + str(take_player_bet(player))

    # 3. 1 card to player, 1 card to dealer (both face up)
    player.cards.append(give_card())
    dealer.cards.append(give_card())
    player.cards.append(give_card())
    dealer.cards.append(give_card())
    print "\n\t%s, your cards are:" \
          "\n\t%s\n\t%s" % (player.name,card_dict[player.cards[0]],card_dict[player.cards[1]])
    #print player.cards
    #print len(player.cards)
    print "\n\tDealer's cards are:" \
          "\n\t%s\n\t%s" % (card_dict[dealer.cards[0]],card_dict[dealer.cards[1]])

    if has_blackjack(player):
        print "\n\t%s, you have blackjack!" % player.name

        if has_blackjack(dealer):
            # Player wins back their money, nothing more
            print "\n\tDealer also has blackjack!" \
                  "\n\tI am giving you back your money."
            player.bankroll += player.bet
            player.bet = 0
            print "\n\tYour money pot is now back to: %s" % str(player.bankroll)

        else:
            # Player wins back their money, plus 3/2 of the bet
            prize = player.bet + (player.bet * 1.5)
            print "\n\t%s, you won!" \
                  "\n\tI am now paying out: %s" % (player.name,str(prize))
            player.bankroll += prize
            player.bet = 0
            print "\n\tYour money pot is now: %s" % str(player.bankroll)

    elif has_blackjack(dealer):
        # Player loses
        print "\n\tDealer has blackjack. %s, you lose this round." % (player.name)
        player.bet = 0

    #print "Dealer Cards:"
    #print dealer.cards
    #print len(dealer.cards)
    if has_blackjack(dealer):
        print "\n\tDealer has blackjack!"


    # 4. 2nd card to player (face up), 2nd card to dealer (face down, unless bj)

    # 5. Check if player/dealer have blackjack

    pass


def main():

    play_game()

# ---- ---- ----

"""
Script execution
"""

init_game()

main()