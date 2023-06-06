import pygame
from single_card import Single_card
GRAY = (200, 200, 200)
CARD_WIDTH = 100
CARD_HEIGHT = 150
CARD_MARGIN = 10
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
        image_path = f"assets/img/{self.name}.webp"
        try:
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
            return image
        except pygame.error:
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
            surface.blit(pygame.transform.scale(self.image, (enlarged_width, enlarged_height)), enlarged_rect)
        else:
            surface.blit(self.image, self.rect)

    def play(self,player):
        print(f"You ({player}) have {player.actions} action, {player.buys} buy, and {player.treasure} treasure")
        player.discard_pile.append(Single_card(self))
        remove_index = 0
        for i,card in enumerate(player.hand):
            if card.card == self:
                remove_index = i
        player.hand.pop(remove_index)