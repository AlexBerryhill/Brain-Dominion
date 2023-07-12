import pygame
from ui.option import Option
from constants import MOVEMENT_KEYS,SELECTION_KEYS,SELECT_MODE,WINDOW_HEIGHT,WINDOW_WIDTH
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
            elif event.type == SELECT_MODE:
                self.manager.game_options.append(Option("Finish Selection",(WINDOW_WIDTH - 90,WINDOW_HEIGHT-50),15))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
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
                    zone = self.get_zone()
                    if self.key_zone == 'hand':
                        card = zone[self.key_index]
                        if self.is_valid_hand_card(card):
                            self.play_from_hand(card)
                    elif self.key_zone == 'options':
                        self.choose_option(zone[self.key_index].text)

                    else:
                        card = self.manager.cards[zone[self.key_index]]
                        if self.is_valid_supply_card(card):
                            self.draw_from_supply(zone[self.key_index],card)

        return True
    
    def handle_key_movement(self,event):
        self.reset_highlights()
        if event.key in MOVEMENT_KEYS[:2]:
            if self.key_zone == 'options':
                if event.key == MOVEMENT_KEYS[0]:
                    self.key_index -= 1
                    if self.key_index < 0:
                        self.key_index = len(self.manager.game_options) - 1
                else:
                    self.key_index += 1
                    if self.key_index >= len(self.manager.game_options):
                        self.key_index = 0
            else:
                self.key_zone = 'hand' if self.key_zone == 'supply' else 'supply'
                self.key_index = 0
        
        zone = self.get_zone()

        if event.key == MOVEMENT_KEYS[2]:
            self.key_index += 1
            if self.key_zone == 'options':
                self.key_zone = 'hand'
                self.key_index = 0
            elif self.key_index >= len(zone):
                if self.key_zone == 'supply':
                    self.key_index = 0
                elif self.key_zone == 'hand':
                    self.key_zone = 'options'
                    self.key_index = 0
        elif event.key == MOVEMENT_KEYS[3]:
            self.key_index -= 1
            if self.key_zone == 'options':
                self.key_zone = 'hand'
                self.key_index = len(self.manager.current_player.hand) - 1
            elif self.key_index <= -1:
                if self.key_zone == 'supply':
                    self.key_index = len(zone) - 1
                elif self.key_zone == 'hand':
                    self.key_zone = 'options'
                    self.key_index = 0
        
        zone = self.get_zone()

        if self.key_zone == 'hand' and  0 <= self.key_index < len(self.manager.current_player.hand):
            card = zone[self.key_index]
            card.selected = True
            if self.is_valid_hand_card(card):
                card.highlighted = True
        elif self.key_zone == 'supply' and 0 <= self.key_index < len(self.manager.supply.keys()):
            card = self.manager.cards[zone[self.key_index]]
            card.selected = True
            if self.is_valid_supply_card(card):
                card.highlighted = True
        elif self.key_zone == 'options' and 0 <= self.key_index < len(zone):
            self.manager.game_options[self.key_index].selected = True
    
    def get_zone(self):
        if self.key_zone == 'hand':
            zone = self.manager.current_player.hand
        elif self.key_zone == 'supply':
            zone = list(self.manager.supply.keys())
        elif self.key_zone == 'options':
            zone = self.manager.game_options
        return zone

            
    def is_valid_hand_card(self,card):
        if card.card.type == "Kingdom" and self.manager.current_player.actions < 1:
            return False
        return card.card.type in self.manager.current_player.valid_card_selection_types and (self.manager.current_player.uses != 0 or not self.manager.current_player.select_mode)

    def is_valid_supply_card(self,card):
        current_player = self.manager.current_player
        return card.cost <= current_player.feast_money or (current_player.buys > 0 and (card.cost <= current_player.treasure)) and card.type in current_player.valid_buy_types

    def handle_click(self,event):
        if event.button == 1:  # Left mouse button
            mouse_pos = pygame.mouse.get_pos()
            # Check if the player clicked on a supply stack
            for card_id in self.manager.supply.keys():
                card = self.manager.cards[card_id]
                if card.rect.collidepoint(mouse_pos):
                    self.draw_from_supply(card_id,card)

            # Check if the player clicked on a card in hand
            for card in self.manager.current_player.hand:
                if card.rect.collidepoint(mouse_pos):
                    self.play_from_hand(card)

            for option in self.manager.game_options:
                if option.rect.collidepoint(mouse_pos):
                    self.choose_option(option.text)
    
    def choose_option(self,text):
        if text == "End Turn":
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN,{'key':pygame.K_e}))
        elif text == "Finish Selection":
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN,{'key':pygame.K_s}))

    def reset(self):
       self.key_mode = False
       self.key_zone = 'hand'
       self.key_index = 0
    
    def draw_from_supply(self,card_id,card):
        if self.manager.cards[card_id].enabled:
            self.manager.current_player.buy_card(card)
            self.manager.supply[card_id] -= 1
    
    def play_from_hand(self,card):
        if card.card.type in self.manager.current_player.valid_card_selection_types:
            card.card.play(self.manager.current_player, self.manager.players, self.manager.cards)

    def reset_highlights(self):
        # Reset highlights
        for card in self.manager.cards:
            card.highlighted = False
            card.selected = False
        
        for card in self.manager.current_player.hand:
            card.highlighted = False
            card.selected = False
        
        for card in self.manager.current_player.discard_pile:
            card.highlighted = False
            card.selected = False
        
        for option in self.manager.game_options:
            option.selected = False



    def handle_hover(self):
        current_player = self.manager.current_player
        mouse_pos = pygame.mouse.get_pos()

        self.reset_highlights()

        for option in self.manager.game_options:
            if option.rect.collidepoint(mouse_pos):
                option.selected = True
        # Check if hovering over player's hand cards
        for card in current_player.hand:
            if card.rect.collidepoint(mouse_pos) and self.is_valid_hand_card(card):
                card.highlighted = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                break
            else:
                card.highlighted = False
        # Check if hovering over supply decks
        # supply_x = CARD_MARGIN
        # supply_y = CARD_MARGIN
        for card_id in self.manager.supply:
            card = self.manager.cards[card_id]
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