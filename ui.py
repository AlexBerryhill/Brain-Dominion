import pygame
from constants import WINDOW_HEIGHT,WINDOW_WIDTH,CARD_HEIGHT,CARD_MARGIN,CARD_WIDTH,HIGHLIGHT_COLOR
from element import Element

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

    def handle_click(self,event):
        if event.button == 1:  # Left mouse button
            mouse_pos = pygame.mouse.get_pos()
            # Check if the player clicked on a supply stack
            for card_id in self.manager.supply.keys():
                card = self.manager.cards[card_id]
                if card.rect.collidepoint(mouse_pos):
                    # Draw a card from the selected supply pile
                    if self.manager.supply[card_id] > 0:
                        self.manager.current_player.buy_card(card)
                        self.manager.supply[card_id] -= 1

            for card in self.manager.current_player.hand:
                if card.rect.collidepoint(mouse_pos) and card.card.type in self.manager.current_player.valid_card_selection_types:
                    card.card.play(self.manager.current_player, self.manager.players, self.manager.cards)

    def handle_hover(self):
        current_player = self.manager.current_player
        mouse_pos = pygame.mouse.get_pos()
        # Reset highlights
        for card in self.manager.cards:
            card.highlighted = False
        
        for card in current_player.hand:
            card.highlighted = False
        
        for card in current_player.discard_pile:
            card.highlighted = False

        # Check if hovering over player's hand cards
        for card in current_player.hand:
            if card.card.type == "Kingdom" and current_player.actions < 1:
                valid_card = False
            else:
                valid_card = card.card.type in current_player.valid_card_selection_types and (current_player.uses != 0 or not current_player.select_mode)
            if card.rect.collidepoint(mouse_pos) and valid_card:
                card.highlighted = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                break
            else:
                card.highlighted = False
        # Check if hovering over supply decks
        else:
            supply_x = CARD_MARGIN
            supply_y = CARD_MARGIN
            for card_id in self.manager.supply:
                card = self.manager.cards[card_id]
                valid_card = current_player.buys > 0 and (card.cost <= current_player.treasure or card.cost <= current_player.feast_money) and card.type in current_player.valid_buy_types
                if card.rect.collidepoint(mouse_pos) and valid_card:
                    card.highlighted = True
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    break
                supply_x += CARD_WIDTH + CARD_MARGIN
                if supply_x + CARD_WIDTH > WINDOW_WIDTH:
                    supply_x = CARD_MARGIN
                    supply_y += CARD_MARGIN + CARD_HEIGHT
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw_cards(self):
        current_player = self.manager.current_player
        # Draw supply stacks with highlighting
        supply_x = CARD_MARGIN
        supply_y = CARD_MARGIN
        for i, card_id in enumerate(self.manager.supply):
            card = self.manager.cards[card_id]
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
