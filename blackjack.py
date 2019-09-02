from collections import namedtuple
from random import shuffle

Card = namedtuple('Card', ('Suit', 'Rank'))


class Deck:

    def __init__(self):
        self.cards = []
        self.construct_deck()

    def construct_deck(self) -> None:
        # Define ranks and Suits
        ranks = [_ for _ in range(2, 11)] + ['Jack', 'Queen', 'King', 'Ace']
        suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
        # Init Deck
        for i in suits:
            for j in ranks:
                self.cards.append(Card(i, j))

    def shuffle(self) -> None:
        shuffle(self.cards)

    def draw(self) -> Card:
        return self.cards.pop()


class Player:

    def __init__(self):
        self.hand = []
        self.count = 0
        self.aces = 0

    def print_hand(self):
        for i in set(self.hand):
            print(i.Rank, " of ", i.Suit, sep='')
        print(self.count, "points")

    # Deal the first two cards of the hand
    def start(self, deck):
        self.hit(deck)
        self.hit(deck)
        self.print_hand()

    # Player input required
    def play(self, deck):
        not_done = True
        while not_done:
            choice = input("Type Hit Or Stay: ")
            if choice == "Hit":
                self.hit(deck)
            elif choice == "Stay":
                self.stay()
                not_done = False
            self.print_hand()
            # check if player busted
            if self.count > 21:
                print("Busted.")
                self.stay()
                not_done = False

    # Dealer's decisions are based on player score
    def dealer_play(self, deck, player_score):
        while self.count < player_score < 22:
            self.hit(deck)
        print("\nDealer hand:")
        self.print_hand()

    def hit(self, deck):
        c = deck.draw()
        self.hand.append(c)
        if c.Rank is 'Ace':
            self.aces += 1
            if self.count > 10:
                self.count += 1
            else:
                self.count += 11
        elif c.Rank in ['Jack', 'Queen', 'King']:
            self.count += 10
        else:
            self.count += c[1]
        # Aces can be 1 or 11 depending on total score
        if self.count > 21 and self.aces == 0:
            self.stay()
        elif self.count > 21:
            self.count -= 10
            self.aces -= 1

    def stay(self) -> int:
        return self.count


def get_winner(p, d) -> bool:
    if p.count > 21:
        print("You busted. Dealer wins")
    elif d.count > 21:
        print("Dealer busted, you win!")
    elif d.count < p.count:
        print("You Won!\n")
    else:
        print("Dealer wins.\n")
    prmpt = input("Continue playing? (Y/N) ")
    if prmpt == "Y":
        return True
    else:
        return False


print("Let's Play Blackjack")
cont = True
while cont:
    deck1 = Deck()
    deck1.shuffle()
    print("\nDealer's turn")
    dealer = Player()
    dealer.start(deck1)
    print("\nYour turn")
    player1 = Player()
    player1.start(deck1)
    player1.play(deck1)
    dealer.dealer_play(deck1,player1.count)
    cont = get_winner(player1, dealer)
print("Thanks for playing!")
