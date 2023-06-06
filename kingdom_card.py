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
                    case 8:
                        self.add_card_to_player_deck(player,cards,1)
                        self.all_discard_one_victory_card(player,players)
                    case _:
                        print("do special action")
            super().play(player)
    
    def add_card_to_player_deck(self,player,cards,card_id):
        player.deck.append(Single_card(cards[card_id]))
        
    def all_discard_one_victory_card(self,player,players):
        for other in players:
            if other != player:
                print()
                remove_i = -1
                for i,card in enumerate(other.hand):
                    print(card)
                    if card.card.type == 'Victory':
                        remove_i = i
                        break
                print()
                if remove_i > -1:
                    other.deck.append(other.hand.pop(remove_i))
                    for card in other.hand:
                        print(card)
