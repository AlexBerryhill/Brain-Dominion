import random
import pygame
from constants import SELECT_MODE
from cards.single_card import Single_card
class Player:
    def __init__(self,cards,name,manager,basis:dict = None ):
        self.manager = manager
        if basis:
            self.deck = self.initialize_ids(cards,basis['deck'])
            self.hand = self.initialize_ids(cards,basis['hand'])
            self.discard_pile = self.initialize_ids(cards,basis['discard_pile'])
            self.name = basis['name']
        else:
            self.deck = []
            self.hand = []
            self.name = name
            self.discard_pile = []
            self.initialize_deck(cards)
            self.draw_cards(5)  # Draw 5 cards at the start of the game

        self.buys = 1
        self.actions = 1
        self.treasure = 0
        self.feast_money = 0
        self.select_mode = False
        self.uses = 0
        self.valid_card_selection_types = ["Treasure","Kingdom"]
        self.valid_buy_types = ["Treasure","Kingdom","Victory"]
    
    def initialize_ids(self,cards,list):
        return [Single_card(cards[id]) for id in list]
    
    def load_current_player_stats(self,stats):
        self.buys = stats['buys']
        self.treasure = stats['treasure']
        self.actions = stats['actions']
        self.uses = stats['uses']
        self.feast_money = stats['feast_money']
        self.select_mode = stats['select_mode']
        self.valid_card_selection_types = stats['selection_types']
        self.valid_buy_types = stats['buy_types']
        

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
    
    def discard_card(self,target_card):
        '''discards the card if found in the hand and returns the index. Returns -1 if not found.'''
        remove_index = -1
        for i,card in enumerate(self.hand):
            if card.card == target_card:
                remove_index = i
        if remove_index != -1: 
            self.discard_pile.append(self.hand.pop(remove_index))
        return remove_index
    
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
        if self.select_mode:
            self.deactivate_selection_mode()
    
    def activate_selection_mode(self,function,uses = -1,valid_selection_types=["Treasure","Kingdom","Victory"]):
        self.valid_card_selection_types =valid_selection_types
        self.uses = uses
        self.select_function = function
        self.select_mode = True
        pygame.event.post(pygame.event.Event(SELECT_MODE))
    
    def deactivate_selection_mode(self):
        self.select_mode = False
        self.valid_card_selection_types = ["Treasure","Kingdom"]
        self.manager.game_options.pop()

    
    def trash_card(self,target_card):
        remove_i = -1
        for i,card in enumerate(self.hand):
            if card.card == target_card:
                remove_i = i
                break
        if remove_i > -1:
            self.hand.pop(remove_i)
        else:
            print("Error finding card to trash")

    def buy_card(self,card):

        if self.feast_money >= card.cost and card.cost > 0:
            self.discard_pile.append(Single_card(card))
            self.feast_money = 0
            self.valid_buy_types = ["Kingdom","Treasure","Victory"]
            return
        if self.buys > 0 and self.treasure >= card.cost:
            self.buys -= 1
            self.treasure -= card.cost
            self.discard_pile.append(Single_card(card))
            return
        if self.buys < 1:
            print("not enough buys")
        if self.treasure < card.cost:
            print("not enough money")
        