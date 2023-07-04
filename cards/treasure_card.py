from cards.card import Card
class Treasure_card(Card):
    def __init__(self, name, cost, worth, id,starting_amount):
        super().__init__(name, cost, "Treasure",id,starting_amount)
        self.worth = worth
    
    def play(self,player,players,cards):
        if super().play(player,players,cards):
            player.treasure += self.worth
            player.discard_card(self)