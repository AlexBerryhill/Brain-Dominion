import pygame
from constants import WINDOW_HEIGHT,WINDOW_WIDTH,CARD_HEIGHT,CARD_MARGIN,CARD_WIDTH,HIGHLIGHT_COLOR,FONT_PATH,BLACK
from ui.element import Element
from ui.option import Option

class UI:
    def __init__(self,manager):
        self.manager = manager
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Dominion")
        background_image = pygame.image.load("./assets/background.jpg")
        self.background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.gui_elements = []
        for text in ["Actions","Buys","Treasure","Player"]:
            self.gui_elements.append(Element(manager,text,0))
        

    def draw_background(self):
        self.window.blit(self.background_image, (0, 0))
    def draw_menu(self,options):
        header = pygame.font.Font(FONT_PATH,50).render("Dominion", True, BLACK)
        self.window.blit(header,(200,100))
        for option in options:
            option.draw(self.window)

    def draw_cards(self):
        current_player = self.manager.current_player
        # Draw supply stacks with highlighting
        supply_x = CARD_MARGIN
        supply_y = CARD_MARGIN
        ran_over = []
        for i, card_id in enumerate(self.manager.supply):
                
            card = self.manager.cards[int(card_id)]
            if card.highlighted:
                pygame.draw.rect(self.window, HIGHLIGHT_COLOR, card.rect, 3)
            card.draw_stack(self.window, supply_x, supply_y)
            supply_x += CARD_WIDTH + CARD_MARGIN
            if supply_x + CARD_WIDTH > WINDOW_WIDTH:
                supply_x = CARD_MARGIN
                supply_y += CARD_MARGIN + CARD_HEIGHT

        # Draw player hand with highlighting
        for i, card in enumerate(current_player.hand):
            card_x = CARD_MARGIN + (CARD_WIDTH + CARD_MARGIN) * i
            card_y = WINDOW_HEIGHT - CARD_MARGIN - CARD_HEIGHT
            if card.highlighted:
                pygame.draw.rect(self.window, HIGHLIGHT_COLOR, card.rect, 3)
            card.draw(self.window, card_x, card_y)
        if len(current_player.discard_pile):
            current_player.discard_pile[-1].draw(self.window, WINDOW_WIDTH - CARD_MARGIN - CARD_WIDTH,WINDOW_HEIGHT - CARD_MARGIN - CARD_HEIGHT * 2)

    def draw_gui(self):
        for element in self.gui_elements:
            element.refresh(self.window)
