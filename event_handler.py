import pygame
from constants import MOVEMENT_KEYS,SELECTION_KEYS
class EventHandler:
    def __init__(self,manager) -> None:
       self.manager = manager
       self.reset()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.manager.current_player.select_mode:
                    print("Cannot exit while in selection mode. Finish using this card and then try again.")
                else:
                    return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event)
            # Change cursor and highlight cards on hover
            elif event.type == pygame.MOUSEMOTION:
                self.handle_hover()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.manager.current_player.end_turn()
                    self.manager.next_player()
                if event.key == pygame.K_s:
                    self.manager.current_player.deactivate_selection_mode()
                if event.key in MOVEMENT_KEYS and not self.key_mode:
                    self.key_mode = True
                if self.key_mode and event.key in MOVEMENT_KEYS:
                    self.handle_key_movement(event)
                if event.key in SELECTION_KEYS:
                    zone = self.manager.current_player.hand if self.key_zone == 'hand' else list(self.manager.supply.keys())
                    if self.key_zone == 'hand':
                        card = zone[self.key_index]
                        if self.is_valid_hand_card(card):
                            self.play_from_hand(card)
                    else:
                        card = self.manager.cards[int(zone[self.key_index])]
                        if self.is_valid_supply_card(card):
                            self.draw_from_supply(str(zone[self.key_index]),card)

        return True
    
    def handle_key_movement(self,event):
        self.reset_highlights()
        if event.key in MOVEMENT_KEYS[:2]:
            self.key_zone = 'hand' if self.key_zone == 'supply' else 'supply'
            self.key_index = 0
        zone = self.manager.current_player.hand if self.key_zone == 'hand' else list(self.manager.supply.keys())
        if event.key == MOVEMENT_KEYS[2]:
            self.key_index += 1
            if self.key_index >= len(zone):
                self.key_index = 0
        elif event.key == MOVEMENT_KEYS[3]:
            self.key_index -= 1
            if self.key_index <= -1:
                self.key_index = len(zone) - 1

        if self.key_zone == 'hand' and  0 <= self.key_index < len(self.manager.current_player.hand):
            card = zone[self.key_index]
            if self.is_valid_hand_card(card):
                card.highlighted = True
        elif self.key_zone == 'supply' and 0 <= self.key_index < len(self.manager.supply.keys()):
            card = self.manager.cards[int(zone[self.key_index])]
            if self.is_valid_supply_card(card):
                card.highlighted = True
            
    def is_valid_hand_card(self,card):
        if card.card.type == "Kingdom" and self.manager.current_player.actions < 1:
            return False
        return card.card.type in self.manager.current_player.valid_card_selection_types and (self.manager.current_player.uses != 0 or not self.manager.current_player.select_mode)

    def is_valid_supply_card(self,card):
        current_player = self.manager.current_player
        return current_player.buys > 0 and (card.cost <= current_player.treasure or card.cost <= current_player.feast_money) and card.type in current_player.valid_buy_types

    def handle_click(self,event):
        if event.button == 1:  # Left mouse button
            mouse_pos = pygame.mouse.get_pos()
            # Check if the player clicked on a supply stack
            for card_id in self.manager.supply.keys():
                card = self.manager.cards[int(card_id)]
                if card.rect.collidepoint(mouse_pos):
                    self.draw_from_supply(card_id,card)

            # Check if the player clicked on a card in hand
            for card in self.manager.current_player.hand:
                if card.rect.collidepoint(mouse_pos):
                    self.play_from_hand(card)
    
    def reset(self):
       self.key_mode = False
       self.key_zone = 'hand'
       self.key_index = 0
    
    def draw_from_supply(self,card_id,card):
        if self.manager.supply[card_id] > 0:
            self.manager.current_player.buy_card(card)
            self.manager.supply[card_id] -= 1
    
    def play_from_hand(self,card):
        if card.card.type in self.manager.current_player.valid_card_selection_types:
            card.card.play(self.manager.current_player, self.manager.players, self.manager.cards)

    def reset_highlights(self):
        # Reset highlights
        for card in self.manager.cards:
            card.highlighted = False
        
        for card in self.manager.current_player.hand:
            card.highlighted = False
        
        for card in self.manager.current_player.discard_pile:
            card.highlighted = False



    def handle_hover(self):
        current_player = self.manager.current_player
        mouse_pos = pygame.mouse.get_pos()

        self.reset_highlights()

        # Check if hovering over player's hand cards
        for card in current_player.hand:
            if card.rect.collidepoint(mouse_pos) and self.is_valid_hand_card(card):
                card.highlighted = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                break
            else:
                card.highlighted = False
        # Check if hovering over supply decks
        else:
            # supply_x = CARD_MARGIN
            # supply_y = CARD_MARGIN
            for card_id in self.manager.supply:
                card = self.manager.cards[int(card_id)]
                if card.rect.collidepoint(mouse_pos) and self.is_valid_supply_card(card):
                    card.highlighted = True
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    break
                # supply_x += CARD_WIDTH + CARD_MARGIN
                # if supply_x + CARD_WIDTH > WINDOW_WIDTH:
                #     supply_x = CARD_MARGIN
                #     supply_y += CARD_MARGIN + CARD_HEIGHT
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)