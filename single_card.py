import copy
class Single_card():
    def __init__(self,card) -> None:
        self.card = card
        self.rect = copy.copy(card.rect)
        self.highlighted = False
    
    def draw(self, surface, x, y):
        self.rect.topleft = (x, y)
        surface.blit(self.card.image, self.rect)
    
    def __str__(self) -> str:
        return self.card.__str__()