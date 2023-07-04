from cards.card import Card
class Victory_card(Card):
    def __init__(self, name, cost, victory_points, id,starting_amount):
        super().__init__(name, cost, "Victory", id,starting_amount)
        self.victory_points = victory_points
    
    def play(self,player,players,cards):
        if super().play(player,players,cards):
            print("you can't play a victory card")