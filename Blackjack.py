# I need shuffle!
import random

#-----------------------------------------------------------------------------------------------
# Deck class

class Deck(object):
    
    standard_deck = ('Ace of Spades', 'Two of Spades', 'Three of Spades', \
        'Four of Spades', 'Five of Spades', 'Six of Spades', 'Seven of Spades', \
        'Eight of Spades', 'Nine of Spades', 'Ten of Spades', 'Jack of Spades', \
        'Queen of Spades', 'King of Spades', 'Ace of Clubs', 'Two of Clubs', \
        'Three of Clubs', 'Four of Clubs', 'Five of Clubs', 'Six of Clubs', \
        'Seven of Clubs', 'Eight of Clubs', 'Nine of Clubs', 'Ten of Clubs', \
        'Jack of Clubs', 'Queen of Clubs', 'King of Clubs', 'Ace of Hearts', \
        'Two of Hearts', 'Three of Hearts', 'Four of Hearts', 'Five of Hearts', \
        'Six of Hearts', 'Seven of Hearts', 'Eight of Hearts', 'Nine of Hearts', \
        'Ten of Hearts', 'Jack of Hearts', 'Queen of Hearts', 'King of Hearts', \
        'Ace of Diamonds', 'Two of Diamonds', 'Three of Diamonds', 'Four of Diamonds', \
        'Five of Diamonds', 'Six of Diamonds', 'Seven of Diamonds', 'Eight of Diamonds', \
        'Nine of Diamonds', 'Ten of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds', \
        'King of Diamonds')

    def __init__(self):
        self.new_game()

    def new_game(self):
        self.new_deck()
        self.shuffle_deck()

    def new_deck(self):
        self.deck = list(Deck.standard_deck)

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def print_deck(self):
        print(self.deck)

    def pull_card(self):
        return self.deck.pop()
        

#-----------------------------------------------------------------------------------------------
# Player class

class Player(object):
    card_values = {'Ace': 11, 'Two': 2, 'Three': 3, 'Four': 4, \
        'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, \
        'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10 }

    def __init__(self):
        self.reset()

    def reset(self):
        "Initialize all values to blank"
        self.total = 0
        self.hand = []
        self.ace_count = 0

    def add_to_total(self, value):
        self.total += value

    def get_total(self):
        return self.total

    def print_hand(self):
        "Print each card on a line as well as their total"
        for card in self.hand:
            print(card)
        print('\nTotal: {}'.format(self.total), end='\n\n')

    def add_card(self, card, display):
        "Add a card to their deck. If it's an ace, keep track of that. Send true or false to display"
        "the pulled card"
        self.hand.append(card)
        self.add_to_total(Player.card_values[card.split()[0]])

        if card.startswith('Ace'):
            self.ace_count += 1

        if display:
            print('Pulled ' + card, end='\n\n')

    def bust(self):
        if self.total <= 21:
            return False
        else:
            return not self.reduce_aces()

    def reduce_aces(self):
        "If there is a soft ace, reduce the total. Return whether or not it was possible to do so"
        if self.ace_count > 0:
            self.ace_count -= 1
            self.total -= 10
            return True
        else:
            return False


#-----------------------------------------------------------------------------------------------
# Game logic

def print_blackjack_introduction():
    "Print game rules"
    print('\f')
    print('Welcome to Blackjack!'.center(120, ' '), end='\n\n')
    print('In Blackjack, the rules are simple: Try to get as close to 21 as you can without going over!'.center(120, ' '), end='\n\n')
    print('You will be playing against the dealer, which means that you need to either beat his hand or'.center(120, ' '))
    print('get 21.'.center(120, ' '), end='\n\n')
    print('You will start with two cards. It is up to you whether you wish to hit or stay. If you stay,'.center(120, ' '))
    print('your turn is over and you must hope that you get higher than what the dealer gets (assuming'.center(120, ' '))
    print('that you did not get to 21). If you hit, that means a card will be added to your hand. You'.center(120, ' '))
    print('can hit as many times as you like, but try not to bust, which is going over 21.'.center(120, ' '), end='\n\n')
    print('Good luck!'.center(120, ' '), end='\n\n\n\n')


def initialize_hands(player, dealer, deck):
    "Gives each player two cards"
    player.add_card(deck.pull_card(), False)
    player.add_card(deck.pull_card(), False)
    dealer.add_card(deck.pull_card(), False)
    dealer.add_card(deck.pull_card(), False)


def game_logic(bet):
    
    # Initialize all game components
    deck = Deck()
    dealer = Player()
    player = Player()

    # Deal out the starting two cards
    initialize_hands(player, dealer, deck)
    if player.get_total() == 21:
        player.print_hand()
        print('21!', end='\n\n')
        return bet * 2

    elif player.get_total() > 21:
        player.reduce_aces()
    
    while True:
        # Display what the player has
        print('\f')
        print('You have:')
        player.print_hand()

        keep_playing = input('(H)it or (s)tay? --> ')
        print()

        # Stay, dealer's turn now
        if keep_playing.lower().startswith('s'):
            break

        # Hit. Add a card
        elif keep_playing.lower().startswith('h'):
            player.add_card(deck.pull_card(), True)

            # If they bust, end the game. If they have 21, move to dealer's turn,
            # Otherwise continue with the player's turn
            if player.bust():
                print('Bust!', end='\n\n')
                return -bet

            elif player.get_total() == 21:
                print('21!', end='\n\n')
                break

            else:
                continue

        # Invalid input, ask again
        else:
            continue

    # Print the dealer's starting hand
    print('Dealer has:')
    dealer.print_hand()

    # Keep drawing cards for the dealer until the total is 17 or more
    while dealer.get_total() < 17:
        dealer.add_card(deck.pull_card(), True)
        if dealer.get_total() > 21 and dealer.bust():
            print('Bust!')
        else:
            print('Total: ' + str(dealer.get_total()), end='\n\n')
    
    # Determine who wins the game
    if player.get_total() > dealer.get_total() or dealer.get_total() > 21:
        print('You win!', end='\n\n')
        if player.get_total() == 21:
            return bet * 2
        return bet

    elif dealer.get_total() == player.get_total():
        print('Draw!', end='\n\n')
        return 0
    else:
        print('You lose!', end='\n\n')
        return -bet


# Flush the screen and print the intro
print('\f')
print_blackjack_introduction()
money = 50
while True:

    # They are allowed to play as long as they have money
    if money > 0:
        play_game = input('Would you like to play? You have ${} ($10 bet). [y/n] --> '.format(money))
        print()

        if play_game.lower().startswith('y'):
            winnings = game_logic(10)
            money += winnings
            if winnings > 0:
                print('You won ${}!'.format(winnings))
            elif winnings == 0:
                print('You keep your bet.')
            else:
                print('You lost ${}!'.format(-winnings))

        elif play_game.lower().startswith('n'):
            print('\f')
            print('Goodbye!', end='\n\n')
            break
        else:
            continue

    else:
        print('\f')
        print('You are out of money! Try again next time!', end='\n\n')
        break

