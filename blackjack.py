import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 
'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 
'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

#CARD DATA AND A PRINT METHOD TO IT

class Card:
    def __init__(self, suit, rank):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f'{self.rank} of {self.suit}'

#DECK CLASS AND METHODS FOR IT

class Deck():
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                self.deck.append(card)

    #DECK SHUFFLE

    def shuffle(self):
        random.shuffle(self.deck)

    def __str__(self) -> str:
        txt = ''
        for l in self.deck:
            txt += f'{l}/'

        return txt

    #PULLED OUT CARD

    def deal(self):
        return self.deck.pop()

#CURRENT HAND

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces += 1

    def show_first_card(self):

        print(f'First card: [{self.cards[0]}]')

    def show_all_cards(self):
        txt = 'All player cards: '
        for i in self.cards:
            txt += f'[{i}] '
        print('Cards:',*self.cards,sep=' | ')

    def stats(self):
        print(f'Total value: {self.value} \n Total aces: {self.aces}')


    #ACE ADJUSTMENT

    def adjust_for_ace(self):
        while self.aces:
            self.aces -= 1
            while True:
                try:
                    option = int(input('1 or 11'))
                    if option == 1:
                        self.value -= 10
                        break
                    elif option == 11:
                        break
                    else:
                        print('Invalid sum')
                        continue
                except:
                    print('Not a num')
                    continue
            # while self.value < 21 and self.aces:
        #     self.value -= 10
        #     self.aces -= 1

#CURRENT AMOUNT OF CHIPS AND BET METHODS

class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0
    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

    def __str__(self) -> str:
        return f'Total chips: {self.total}'


#CHIPS TO BET

def bet_in(chips):
    
    while True:
        try:
            chips.bet = int(input('How many chips are you gonna bet in?'))
        except:
            print('Sorry, this is not an integer')
        else:
            if chips.bet <= chips.total:
                return True
            else:
                print(f'You are broke! \nBalance: {chips.total}')
                return False
                
#ADD A CARD TO YOUR HAND

def add_to_hand(player, deck):
    player.add_card(deck.deal())

#HIT OR STAY

def choose_what_to_do(player, deck):
    while True:
        choice = input('Do you wish to add cards? [Y/N]')
        if choice.upper() == 'Y':
            player.add_card(deck.deal())
            player.show_all_cards()
            player.adjust_for_ace()
            player.stats()
            continue
        elif choice.upper() == 'N':
            break
        else:
            print('The answer is not clear')
            continue


#MY CHIPS
my_chips = Chips()

#CARDS
deck_of_cards = Deck()
deck_of_cards.shuffle()

#BLACKJACK GAME
game_on = True

while game_on:

    #ME
    myself = Hand()

    #BOT
    dealer = Hand()

    #CHECKS FOR ENOUGH CARDS
    if len(deck_of_cards.deck) < 4:
        deck_of_cards = Deck()
        deck_of_cards.shuffle()

    #BET AMOUNT
    permission = bet_in(my_chips)
    if permission:
        pass
    else:
        break

    #BET CHECKER
    if my_chips.bet <= 0 or my_chips.total < 0:
        game_on = False
        break

    #CARDS FOR ME
    add_to_hand(myself, deck_of_cards)
    add_to_hand(myself, deck_of_cards)

    #CARDS FOR BOT
    add_to_hand(dealer, deck_of_cards)
    add_to_hand(dealer, deck_of_cards)

    #SHOW DEALER CARD
    print('Dealer card:')
    dealer.show_first_card()

    #SHOW MY CARDS AND STATISTICS
    print('Player cards:')
    myself.show_all_cards()
    myself.stats()

    #CHECK IF i HAVE AN ACE TO ADJUST
    myself.adjust_for_ace()

    #CHOOSE HOW TO CONTINUE
    choose_what_to_do(myself,deck_of_cards)

    #DEALER CHECKS IF HE NEEDS TO ADD CARDS
    while myself.value > dealer.value and dealer.value < 21 and myself.value < 21:
        dealer.add_card(deck_of_cards.deal())

    #WIN CONDITION

    #BOTH ARE BELOW 21
    if dealer.value <=21 and myself.value <= 21:

        if myself.value > dealer.value:
            print('THE PLAYER HAS WON!')
            my_chips.win_bet()
        elif dealer.value > myself.value:
            print('THE DEALER HAS WON!')
            my_chips.lose_bet()
        elif dealer.value == myself.value:
            print('NOBODY WINS!')

        print('Dealer: ')
        dealer.show_all_cards()
        dealer.stats()
        print('Me: ')
        myself.show_all_cards()
        myself.stats()
        
        print(my_chips)

    #BOTH ARE ABOVE 21
    elif dealer.value > 21 or myself.value > 21:
        
        if dealer.value > 21 and myself.value > 21:
            print('NOBODY WINS! BOTH BUSTED!')
        elif myself.value > 21:
            print('THE DEALER HAS WON! THE PLAYER BUSTED!')
            my_chips.lose_bet()
        elif dealer.value > 21:
            print('THE PLAYER HAS WON! THE DEALER BUSTED! ')
            my_chips.win_bet()
        
        print('Dealer: ')
        dealer.show_all_cards()
        dealer.stats()
        print('Me: ')
        myself.show_all_cards()
        myself.stats()
        
        print(my_chips)
    
    #GAME ASKS IF YOU WANT TO KEEP PLAYING
    while True:
        choice = input('Wanna play again? [Y/N]')
        if choice.upper() == 'Y':
            break
        elif choice.upper() == 'N':
            game_on = False
            break
        else:
            print('The answer is not clear')
            continue
