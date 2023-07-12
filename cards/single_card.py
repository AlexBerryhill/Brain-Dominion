import copy
import pygame
from constants import GRAY

CARD_WIDTH = 100
CARD_HEIGHT = 150
CARD_MARGIN = 10
class Single_card():
    def __init__(self,card) -> None:
        self.card = card
        self.rect = copy.copy(card.rect)
        self.highlighted = False
        self.selected = False
    
    def draw(self, surface, x, y):
        self.rect.topleft = (x, y)
        surface.blit(self.card.image, self.rect)
        if self.highlighted:
            # Increase the size of the card when hovered
            enlarged_width = int(CARD_WIDTH * 1.2)
            enlarged_height = int(CARD_HEIGHT * 1.2)
            enlarged_rect = pygame.Rect(x - (enlarged_width - CARD_WIDTH) // 2, y - (enlarged_height - CARD_HEIGHT) // 2, enlarged_width, enlarged_height)
            surface.blit(self.card.big_image, enlarged_rect)
            if self.selected:
                pygame.draw.rect(surface,GRAY,enlarged_rect,width=4)
        else:
            surface.blit(self.card.image, self.rect)
            if self.selected:
                pygame.draw.rect(surface,GRAY,self.rect,width=4)
    
    def __str__(self) -> str:
        return self.card.__str__()