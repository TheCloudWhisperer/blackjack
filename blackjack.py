#!/usr/local/bin/python

#
## Imports
#

# We'll need to shuffle the card deck
from random import shuffle as sh
# Importing my own class definitions
import bj_classes as bjc
# We'll need to know which OS we are running on
from sys import platform
# We will want to clear the screen from time to time
from os import system


# ---- ---- ----


#
## Global Variables:
#

# The "source deck" is the full, ordered deck of cards - this should never change,
# hence we define it as a tuple - now moved to file bj_classes, imported as "bjc".

# The "playing deck" is the deck currently in use - it will be 'populated' with the
# cards from the "source deck" (now defined in the "bj_classes.py" file, imported
# as "bjc") and then shuffled every time.
playing_deck = []

# Let's also have a dictionary to translate short card notation into human notation
# Now moved to file "bj_classes", imported as "bjc"

# Not sure if I will need this - may use to keep track of the cards that have already
# been drawn from the deck in play - commenting out for now...
# drawn_cards = []

# Defining the Dealer and Player objects as global, so that any function can modify
# the same object.
dealer = bjc.Participant()
player = bjc.Player()


# ---- ---- ----


#
## Supporting functions
#


"""
Clearing the screen
"""
def clear_screen():
    """
    This function clears the screen.
    We capture what system (Windows, Linux, OS X) the game is running
    on in a global var with the init_game() function. We also set in the
    same function the correct command to clear the screen.
    This should be called after every move (if the move is valid), before
    the board is updated and printed out again.
    """

    # Let's see which OS we are running on:
    op_sys = platform

    # Let's set the correct command to clear the screen
    if op_sys == 'darwin':
        clr_comm = 'clear'
    else:
        clr_comm = 'not set'

    dummy_var = system(clr_comm)


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
def add_money(entity):

    valid_answer = False

    while not valid_answer:

        try:
            amount = int(raw_input("\n\tHow much money do you want to add to your pot? [Press Enter to confirm]: $"))
            # except ValueError as ex:

        except ValueError:
            print "\n\tI am afraid that is not a valid amount." \
                  "\n\tPlease try again!"

        else:
            print "\n\tThank you, I added that to your pot!"
            entity.bankroll += amount
            valid_answer = True
            dummy_var = raw_input("\n\tPlease press Enter to continue! ")


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

            print "\n\tI have now taken $%s out of your money pot." \
                  "\n\tYour remaining pot is: $%s" % (str(amount), str(entity.bankroll))

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

    valid_bet = False

    clear_screen()

    if entity.bankroll == 0:
        answer = raw_input("\n\tYou currently have no funds, would you like to add some? [y/N]: ")

        if answer.lower() in ('y', 'yes'):   # add other checks, like capital Y, etc...
            add_money(entity)

        else:
            print "\n\tSince you have no funds and no intention to add any, your game ends here!" \
                  "\n\tThank you for playing %s!\n" % (entity.name)
            exit(100)

    while not valid_bet:
        # Asking the player to bet

        try:
            bet = int(raw_input("\n\tPlease, place your bet! [Press Enter to confirm]: $"))

        except ValueError as ex:
            print "\n\tI am afraid that was not a valid bet." \
                  "\n\tPlease try again!"

        else:
            if bet > entity.bankroll:
                print "\n\tI am afraid do not have sufficient funds." \
                      "\n\tYou currently have $%s at your disposal." \
                      "\n\tPlease try again!" % (entity.bankroll)

            else:
                take_money(entity, bet)
                #We record the player's bet, so that we can calculate their wins
                entity.bet = bet
                valid_bet = True
                dummy_var = raw_input("\n\tPlease press Enter to receive your cards! ")

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

    playing_deck = list(bjc.base_deck)

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


"""
A little function to deal with the Dealer's Ace insurance
"""
def ace_insurance(entity):

    valid_answer = False
    valid_amount = False

    while not valid_answer:
        # Asking the player to bet
        answer = raw_input("\n\tDealer's first card is an Ace!"
                           "\n\tDo you want to buy insurance? [y/N]: ")

        if answer.lower() in ('y', 'yes'):
            valid_answer = True

            while not valid_amount:
            # Asking the player for insurance amount

                try:
                    amount = int(raw_input("\n\tHow much insurance do you want to buy? [Press Enter to confirm]: $"))

                except ValueError as ex:
                    print "\n\tI am afraid that was not a valid amount." \
                          "\n\tPlease try again!"

                else:
                    if amount > (entity.bet / 2):
                        print "\n\tI am afraid you cannot buy insurance bigger than $%s" \
                              "\n\tYour bet is currently $%s" \
                              "\n\tPlease try again!" % (str(entity.bet/2), str(entity.bet))

                    elif amount > entity.bankroll:
                        print "\n\tI am afraid your funds won't stretch that far!" \
                              "\n\tYour current money pot is $%s" \
                              "\n\tPlease try again!" % (str(entity.bankroll))

                    else:
                        take_money(entity, amount)
                        # We record the player's insurance, so that we can calculate their wins
                        entity.insurance = amount
                        entity.has_insurance = True
                        valid_amount = True

        elif answer.lower() in ('n', 'no', ''):
            valid_answer = True
            print "\n\tVery well, let's keep playin'!"

        else:
            print "\n\tI did not get that, let's try again..."


"""
A smart function that prints:
- all the Player's cards
- the Dealer's cards depending on stage of game (hole card yes/no)
"""

def print_cards(entity,boolean):

    global player
    global dealer

    hole_card = boolean

    if entity == player:
        is_dealer = False

    elif entity == dealer:
        is_dealer = True

    else:
        print "\n\tSomething went wrong!\n\tExiting!"
        exit (300)

    if not is_dealer:
        print "\n\t%s, your cards are:" % (entity.name)
        for card in entity.cards:
            print "\t" + bjc.card_dict[card]

    else:
        if hole_card:
            print "\n\tDealer's cards are:" \
                  "\n\t%s\n\t%s" % (bjc.card_dict[dealer.cards[0]],"'Hole card'")

        else:
            print "\n\tDealer's cards are:"
            for card in entity.cards:
                print "\t" + bjc.card_dict[card]


"""
Let's have a function that takes care of the first 2 cards...
"""
def two_cards():

    """
    Simulate the first 2 cards, where blackjack can be achieved.
    :return: False if the game is over (eg. one has blackjack, True if the game
             can continue.
    """

    global player
    global dealer

    # 3. 1 card to player, 1 card to dealer (both face up)
    player.cards.append(give_card())
    dealer.cards.append(give_card())


    # 4. 2nd card to player (face up), 2nd card to dealer
    player.cards.append(give_card())
    dealer.cards.append(give_card())

    # Print out cards for the first time
    # Dealer's 2nd card is face down
    clear_screen()
    print_cards(player, False)
    print_cards(dealer, True)


    # 5. In case Dealer's 1st card is an Ace, Player can get insurance
    if dealer.cards[0][0] == 'A':
        ace_insurance(player)


    # 6. Check if player/dealer have blackjack
    if has_blackjack(player):
        print "\n\t%s, you have blackjack!" % player.name

        if has_blackjack(dealer):
            # Player wins back their money, nothing more

            # Printing dealer's blackjack message:
            print "\n\tDealer also has blackjack!"

            # Showing all cards!
            dummy_var = raw_input("\n\tPress Enter to see Dealer's cards: ")
            clear_screen()
            print_cards(player, False)
            print_cards(dealer, False)

            # Sorting out the player's funds:
            player.bankroll += player.bet
            player.bet = 0
            print "\n\tI am giving you back your bet ($%s)." % str(player.bet)

            if player.has_insurance:
                print "\n\tYou bought insurance, I am now also paying out that!" \
                      "\n\tYour insurance was $%s, so I am now paying out $%s" % \
                      (player.insurance, player.insurance * 2)
                player.bankroll += player.insurance * 2
                player.insurance = 0
                print "\n\tYour money pot is now: $%s" % str(player.bankroll)

            else:
                print "\n\tYour money pot is now back to: $%s" % str(player.bankroll)

            return False

        else:
            # Player wins back their money, plus 3/2 of the bet
            #prize = player.bet + (player.bet * 1.5)
            print "\n\tYou won!" \
                  "\n\tI am now paying out: $%s" % (str(player.bet * 1.5))
            player.bankroll += player.bet * 1.5
            player.bet = 0
            print "\n\tYour money pot is now: $%s" % str(player.bankroll)

            return False

    elif has_blackjack(dealer):
        # Player loses

        # Printing dealer's blackjack message:
        print "\n\tDealer has blackjack. %s, you lose this round." % (player.name)

        # Showing all cards!
        dummy_var = raw_input("\n\tPress Enter to see Dealer's cards: ")
        clear_screen()
        print_cards(player, False)
        print_cards(dealer, False)

        # Player loses money he had bet - nothing happens to the money pot
        player.bet = 0

        if player.has_insurance:
            print "\n\tYou lost your bet, but luckily you had bought insurance... I am now paying that out!" \
                  "\n\tYour insurance was $%s, so I am now paying back $%s" % \
                  (player.insurance, player.insurance * 2)
            player.bankroll += player.insurance * 2
            player.insurance = 0

        print "\n\tYour money pot is now: $%s" % str(player.bankroll)

        return False

    else:
        # If we're here neither has blackjack and the game can continue
        return True


"""
This function counts the points in hand for either the Player or the Dealer.
It has to keep into account the different values and Ace can have, and has to
detect whether the Player or Dealer goes bust. 
"""
def count_points(entity):
    pass

"""
This is the function invoked if the player decides to hit another card
"""
def hit_me():
    pass


"""
This function is invoked if the player stays - it may actually not be required,
as there is nothing for the player to do and the turn goes to the Dealer
"""
def staying():
    pass


"""
This is the function invoked when it's the Dealer's turn to draw more cards.
The Dealer does not have much choice and has to observe some specific rules
based on his/her current score - see blackjack rules!
"""
def dealer_draw():
    pass



# ---- ---- ----



"""
Main game functions
"""

def init_game():

    global player

    clear_screen()
    player.name = ask_player_name()

    # Let's add some funds
    clear_screen()
    bankroll_setup(player)


def play_game():

    global player
    global dealer

    # 1. Shuffling the cards
    init_game_deck()

    # 2. Player bet
    take_player_bet(player)

    # We're now playing the initial 2 cards - that function will take care of
    # detecting and rewarding blackjack; if blackjack is achieved, then the
    # "game_on" variable is set to False and the rest of the game does not
    # go ahead.
    game_on = two_cards()

    # We are also using a variable to determine whether we are still in the
    # 2 cards scenario (in which case the player can still surrender), or
    # already past that point.
    has_two_cards = True

    # 7. If we're here, neither has blackjack and a few things can happen:
    #    a. Dealer's 1st card is an Ace, player may want to get insurance
    #    [moved up!!]
    #    b. Player may want to: Stand, Hit, Double, Split, Surrender
    #    c. If player keeps playing, he may "bust" (ie. go over 21)
    #    d. If player Stands, Dealer will need to draw cards according to rules
    #    e. Dealer may win or "bust"

    # We may need a function counting points, so that we can compare them

    while game_on:
        # If we're here then no one has blackjack - do we still only have 2
        # cards (in which case the player can still surrender) or not?
        if has_two_cards:
            print "\n\tHow do you want to play? You can:" \
                  "\n\tStand (s)" \
                  "\n\tHit (h)" \
                  "\n\tSurrender (x)"

            valid_play = False
            while not valid_play:
                play = raw_input("\n\tMake your choice [s,h,x]: ")

                if play.lower() not in ('s', 'h', 'x'):
                    print "\n\tI am sorry, that was not a valid choice. Let's try again!"

                elif play.lower() == 's':
                    print "Staying!"
                    valid_play = True

                elif play.lower() == 'h':
                    print "Hit me!"
                    valid_play = True

                elif play.lower() == 'x':
                    # Debug
                    #print "I surrender!"

                    valid_play = True
                    game_on = False
                    player.bankroll += player.bet / 2.0
                    print "\n\tYou decided to surrender 1/2 of your bet ($%s)." \
                          "\n\tI am now returning $%s to your money pot." \
                          "\n\n\tYour money pot is now: $%s" % (player.bet, (player.bet / 2.0), player.bankroll)
                    player.bet = 0

        else:
            print "\n\tHow do you want to play? You can:" \
                  "\n\tStand (s)" \
                  "\n\tHit (h)"

            valid_play = False
            while not valid_play:
                play = raw_input("\n\tMake your choice [s,h]: ")

            if play.lower() not in ('s', 'h'):
                print "\n\tI am sorry, that was not a valid choice. Let's try again!"

            elif play.lower() == 's':
                print "Staying!"
                valid_play = True

            elif play.lower() == 'h':
                print "Hit me!"
                valid_play = True

        # Debug
        print "\n\tYour choice: %s" % (play)


def main():

    init_game()

    ## The below will need to be invoked in a loop.
    #+ Each time, the player should have the following options:
    #+ 1. Add funds to money pot
    #+ 2. Bet (ie. start a new game)
    #+ 3. Cash out their wins
    play_game()

# ---- ---- ----

"""
Script execution
"""

main()