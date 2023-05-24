from dominion import Card

class Stack():
    def __init__(self,card:Card,count=10):
        '''Starts with 10 because all kingdom cards have 10, other cards must change the original count'''
        self.card = card
        self.count = count

    def draw_card(self):
        self.count -= 1
        return self.card
        
