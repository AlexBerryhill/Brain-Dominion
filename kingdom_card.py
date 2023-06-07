from card import Card
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
    
    def play(self,player,players,cards):
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
                        self.all_discard_one_victory_card(player,players)
                    case 9:
                        pass
                    case 10:
                        player.discard_pile.extend(player.deck)
                    case 11:
                        pass
                    case 12:
                        [other.draw_cards(1) for other in players if other != player]
                    case 13:
                        self.trash(player)
                        player.feast_money = 5
                    case 17:
                        pass
                    case 19:
                        
                        for other in players:
                            if other != player:
                                other.hand = other.hand[:3]
                    case 20:
                        pass
                    case 21:
                        pass
                    case 22:
                        pass
                    case 23:
                        pass
                    case 25:
                        pass
                    case 26:
                        pass
                    case 27:
                        pass
                    case 29:
                        for other in players:
                            if other != player:
                                other.deck.insert(Single_card(cards[6]),0)

                    case _:
                        print("do special action")
            super().play(player)
    
    def add_cards_to_hand(self,player,type,number):
        for _ in range(number):
            while True:
                player.draw_cards(1)
                if player.hand[-1].card.type != type:
                    player.discard_pile.append(player.hand.pop())
                else:
                    break

    def add_card_to_player_deck(self,player,cards,card_id):
        player.deck.append(Single_card(cards[card_id]))
    
    def trash(self,player):
        remove_i = -1
        for i,card in enumerate(player.hand):
            if card.card == self:
                remove_i = i
                break
        if remove_i > -1:
            player.hand.pop(remove_i)
        else:
            print("Error finding card to trash")
    
    def to_all_other_players(self,function,player,players):
        for other in players:
            if other != player:
                function(other)
                print(other.hand)

        
    def all_discard_one_victory_card(self,player,players):
        for other in players:
            if other != player:
                remove_i = -1
                for i,card in enumerate(other.hand):
                    if card.card.type == 'Victory':
                        remove_i = i
                        break
                if remove_i > -1:
                    other.deck.append(other.hand.pop(remove_i))

                    for card in other.hand:
                        print(card)
