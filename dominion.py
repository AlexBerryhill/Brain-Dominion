import pygame
from card_loading import load_cards,setup_game_cards
from player import Player
from constants import NUM_PLAYERS,WINDOW_HEIGHT,WINDOW_WIDTH
from ui import UI

class Master:
    def __init__(self):
        pygame.init()
        self.ui = UI(self)
        self.cards = load_cards()
        self.supply = setup_game_cards(self.cards)
        self.players = [Player(self.cards,i+1) for i in range(NUM_PLAYERS)]

        self.current_player_index = -1
        self.next_player()
        self.run_game()
        pygame.quit()

    def next_player(self):
        if self.current_player_index == len(self.players) - 1:
            self.current_player_index = 0
        else:
            self.current_player_index += 1
        self.current_player = self.players[self.current_player_index]
        self.current_player.start_turn()
        
    def run_game(self):
        while True:
            # Draw the background image
            self.ui.draw_background()
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.ui.handle_click(event)
                # Change cursor and highlight cards on hover
                elif event.type == pygame.MOUSEMOTION:
                    self.ui.handle_hover()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.current_player.end_turn()
                        self.next_player()
                    if event.key == pygame.K_s:
                        self.current_player.deactivate_selection_mode()
            # Draw Supply Stacks and Player Hand
            self.ui.draw_cards()
            # Draw the GUI
            self.ui.draw_gui()

            # Update the display
            pygame.display.flip()

if __name__ == "__main__":
    Master()
