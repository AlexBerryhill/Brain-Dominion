from card import Card
from player import Player
from single_card import Single_card
class Kingdom_card(Card):
    def __init__(self, name, cost, description, plus_actions, plus_treasure, plus_buys, plus_cards, is_attack, is_reaction, id,special_action):
        super().__init__(name, cost, "Kingdom", id,10)
        self.description = description
        self.plus_actions = plus_actions
        self.plus_treasure = plus_treasure
        self.plus_buys = plus_buys
        self.plus_cards = plus_cards
        self.is_attack = is_attack
        self.is_reaction = is_reaction
        self.special_action = special_action
    
    def play(self,player : Player,players,cards):
        if super().play(player,players,cards):
            if player.actions > 0:
                player.actions -= 1
                player.buys += self.plus_buys
                player.actions += self.plus_actions
                player.treasure += self.plus_treasure
                player.draw_cards(self.plus_cards)
                if self.special_action:
                    match self.id:
                        case 7:
                            self.add_cards_to_hand(player,"Treasure",2)

                        case 8:
                            self.add_card_to_player_deck(player,cards,1)
                            # self.all_discard_one_victory_card(player,players)
                            self.attack(self.discard_victory_card,player,players,cards)
                        case 9:
                            player.activate_selection_mode(self.cellar)
                        case 10:
                            player.discard_pile.extend(player.deck)
                        case 11:
                            player.activate_selection_mode(lambda player,card,players,cards:player.trash_card(card),4)
                        case 12:
                            [other.draw_cards(1) for other in players if other != player]
                        case 13:
                            player.trash_card(self)
                            player.feast_money = 5
                        case 17:
                            amount = 7 - len(player.hand)
                            player.draw_cards(amount)
                            player.activate_selection_mode(lambda player,card,players,cards:player.discard_card(card),valid_card_types=["Kingdom"])
                        case 19:
                            # for other in players:
                            #     if other != player and other.discard_card(cards[21]) == -1:
                            #         other.hand = other.hand[:3]
                            self.attack(self.militia,player,players,cards)
                        case 20:
                            player.activate_selection_mode(self.mine,1,["Treasure"])
                        case 21:
                            pass
                        case 22:
                            player.activate_selection_mode(self.money_lender,1,["Treasure"])
                        case 23:
                            player.activate_selection_mode(self.remodel,1)
                        case 25:
                            pass
                        case 26:
                            pass
                        case 27:
                            player.activate_selection_mode(self.throne_room,1,["Kingdom"])
                        case 29:
                            for other in players:
                                if other != player:
                                    other.deck.insert(Single_card(cards[6]),0)
                        case 31:
                            player.feast_money = 4
                        case _:
                            print("do special action")
                player.discard_card(self)
    

    def add_cards_to_hand(self,player,type,number):
        for _ in range(number):
            while True:
                player.draw_cards(1)
                if player.hand[-1].card.type != type:
                    player.discard_pile.append(player.hand.pop())
                else:
                    break
    
    def militia(self,other):
        other.hand = other.hand[:3]
    def cellar(self,player,card,players,cards):
        player.discard_card(card)
        player.draw_cards(1)
    
    def money_lender(self,player:Player,card:Card,players,cards):
        if card.id == 0:
            player.trash_card(card)
            player.treasure += 3

    def throne_room(self,player:Player,card:Card,players,cards):
        if card.id != 27 and card.type == "Kingdom":
            player.actions += 2
            card.play(player,players,cards)
            card.play(player,players,cards)

    def remodel(self,player:Player,card:Card,players,cards):
        player.trash_card(card)
        player.feast_money = card.worth + 2

    def mine(self,player:Player,card,players,cards):
        if 0 <= card.id < 2:
            player.trash_card(card)
            player.feast_money = 3 + card.cost
            player.valid_buy_types = ["Treasure"]
    
    def add_card_to_player_deck(self,player,cards,card_id):
        player.deck.append(Single_card(cards[card_id]))
    
    # def trash(self,player):
    #     remove_i = -1
    #     for i,card in enumerate(player.hand):
    #         if card.card == self:
    #             remove_i = i
    #             break
    #     if remove_i > -1:
    #         player.hand.pop(remove_i)
    #     else:
    #         print("Error finding card to trash")
    
    def attack(self,function,player,players,cards):
        for other in players:
            if other != player and other.discard_card(cards[21]):
                function(other)
                print(other.hand)

    def discard_victory_card(self,other):
        remove_i = -1
        for i,card in enumerate(other.hand):
            if card.card.type == 'Victory':
                remove_i = i
                break
        if remove_i > -1:
            other.deck.append(other.hand.pop(remove_i))

        
    # def all_discard_one_victory_card(self,player,players):
    #     for other in players:
    #         if other != player:
    #             remove_i = -1
    #             for i,card in enumerate(other.hand):
    #                 if card.card.type == 'Victory':
    #                     remove_i = i
    #                     break
    #             if remove_i > -1:
    #                 other.deck.append(other.hand.pop(remove_i))

    #                 for card in other.hand:
    #                     print(card)
