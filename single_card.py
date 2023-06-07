import copy
import pygame

CARD_WIDTH = 100
CARD_HEIGHT = 150

class Single_card():
    def __init__(self,card) -> None:
        self.card = card
        self.rect = copy.copy(card.rect)
        self.highlighted = False
    
    def draw(self, surface, x, y):
        # self.rect.topleft = (x, y)
        # surface.blit(self.card.image, self.rect)
        if self.highlighted:
            # Increase the size of the card when hovered
            enlarged_width = int(CARD_WIDTH * 1.2)
            enlarged_height = int(CARD_HEIGHT * 1.2)
            enlarged_rect = pygame.Rect(x - (enlarged_width - CARD_WIDTH) // 2, y - (enlarged_height - CARD_HEIGHT) // 2, enlarged_width, enlarged_height)
            surface.blit(pygame.transform.scale(self.card.image, (enlarged_width, enlarged_height)), enlarged_rect)
        else:
            self.rect.topleft = (x, y)
            surface.blit(self.card.image, self.rect)
    
    def __str__(self) -> str:
        return self.card.__str__()