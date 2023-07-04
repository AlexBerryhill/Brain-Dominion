import pygame
from cards.single_card import Single_card
from player import Player
from constants import GRAY,CARD_HEIGHT,CARD_WIDTH
class Card:
    def __init__(self, name, cost, type,id,starting_amount):
        self.name = name
        self.cost = cost
        self.type = type
        self.id = id
        self.worth = 0
    
        self.victory_points = 0
        self.starting_amount = starting_amount
        self.special_action = False
        self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)
        self.image = self.load_image()
        self.highlighted = False

    def __str__(self):
        return self.name

    def load_image(self):
        try:
            image_path = f"assets/img/{self.name}.jpg"
            image = pygame.image.load(image_path).convert_alpha()
            enlarged_width = int(CARD_WIDTH * 1.2)
            enlarged_height = int(CARD_HEIGHT * 1.2)
            self.big_image = pygame.transform.smoothscale(image, (enlarged_width, enlarged_height))
            image = pygame.transform.smoothscale(image, (CARD_WIDTH, CARD_HEIGHT))
            
            return image
        except (pygame.error, FileNotFoundError):
            # If image loading fails, create a placeholder image
            image = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
            image.fill(GRAY)
            pygame.draw.rect(image, (0, 0, 0), image.get_rect(), 3)
            return image

    def draw_stack(self, surface, x, y):
        self.rect.topleft = (x, y)
        if self.highlighted:
            # Increase the size of the card when hovered
            enlarged_width = int(CARD_WIDTH * 1.2)
            enlarged_height = int(CARD_HEIGHT * 1.2)
            enlarged_rect = pygame.Rect(x - (enlarged_width - CARD_WIDTH) // 2, y - (enlarged_height - CARD_HEIGHT) // 2, enlarged_width, enlarged_height)
            surface.blit(self.big_image, enlarged_rect)
        else:
            surface.blit(self.image, self.rect)

    def play(self,player:Player,players,cards):
        if player.select_mode and player.uses != 0:
            player.uses -= 1
            player.select_function(player,self,players,cards)
            if player.uses == 0:
                player.deactivate_selection_mode()
            print('select mode used',player.uses,"remaining")
            return False
        return True