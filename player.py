import random
from single_card import Single_card
class Player:
    def __init__(self,cards):
        self.deck = []
        self.hand = []
        self.discard_pile = []
        self.buys = 1
        self.actions = 1
        self.treasure = 0
        self.feast_money = 0
        self.initialize_deck(cards)
        self.draw_cards(5)  # Draw 5 cards at the start of the game

    def initialize_deck(self,cards):
        # Add starting cards to the deck
        self.deck = [Single_card(cards[0]) for _ in range(7)]
        self.deck += [Single_card(cards[3]) for _ in range(3)]
        random.shuffle(self.deck)

    def draw_cards(self, num_cards):
        # Draw a specified number of cards from the deck
        for _ in range(num_cards):
            if len(self.deck) == 0:
                # If the deck is empty, shuffle the discard pile and add it to the deck
                self.deck = self.discard_pile
                self.discard_pile = []
                random.shuffle(self.deck)
            if len(self.deck) > 0:
                card = self.deck.pop()
                self.hand.append(card)
    
    def print_hand(self):
        for card in self.hand:
            print(card)
    def start_turn(self):
        self.buys = 1
        self.actions = 1
        self.treasure = 0

    def end_turn(self):
        self.discard_pile.extend(self.hand)
        self.hand = []
        self.draw_cards(5)
    
    def buy_card(self,card):

        if self.feast_money >= card.cost:
            self.discard_pile.append(Single_card(card))
            print("successfully bought",card)
            self.feast_money = 0
            return
        if self.buys > 0 and self.treasure >= card.cost:
            self.buys -= 1
            self.treasure -= card.cost
            self.discard_pile.append(Single_card(card))
            print("successfully bought",card)
            return
        if self.buys < 1:
            print("not enough buys")
        if self.treasure < card.cost:
            print("not enough money")
        