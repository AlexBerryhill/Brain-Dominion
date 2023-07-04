import pygame, json
from cards.card_loading import load_cards,setup_game_cards,jsonify_card_list
from player import Player
from constants import NUM_PLAYERS,WINDOW_HEIGHT,WINDOW_WIDTH
from ui.ui import UI
from ui.option import Option
from event_handler import EventHandler

class Master:
    def __init__(self):
        pygame.init()
        self.ui = UI(self)
        with open('save_files/saved_files.txt','r') as file:
            self.num_saved_files = int(file.read())
            
        self.options = [Option("Create New Save",(200,200))]
        for file_num in range(1,self.num_saved_files + 1):
            self.options.append(Option(f"Save {file_num}",(200,200 + 60 * file_num)))
        self.save_file = self.run_menu_screen()
        if self.save_file != -1:
            self.cards = load_cards()
            self.load_game(self.save_file)
            self.event_handler = EventHandler(self)
            self.run_game()
            self.save_game()
        pygame.quit()
    
    def save_game(self):
        
        if self.save_file:
            save_file_name = f'save_files/save_{self.save_file}.json'
        else:
            with open('save_files/saved_files.txt','w') as file:
                file.write(str(self.num_saved_files + 1))
            save_file_name = f'save_files/save_{len(self.options)}.json'
        saved_game = {
            "supply":self.supply,
            "current_player_index":self.current_player_index,
            "players":[],
            "current_player_stats":{
                "buys":self.current_player.buys,
                "treasure":self.current_player.treasure,
                "actions":self.current_player.actions,
                "select_mode":self.current_player.select_mode,
                "feast_money":self.current_player.feast_money,
                "uses":self.current_player.uses,
                "selection_types":self.current_player.valid_card_selection_types,
                "buy_types":self.current_player.valid_buy_types
            }
        }
        for player in self.players:
            player_stats = {
                "hand":jsonify_card_list(player.hand),
                "discard_pile":jsonify_card_list(player.discard_pile),
                "deck":jsonify_card_list(player.deck),
                "name":player.name
            }
            saved_game["players"].append(player_stats)

        with open(save_file_name,'w') as file:
            json.dump(saved_game,file)


    def load_game(self,save_file):
        if save_file == 0:
            self.supply = setup_game_cards(self.cards)
            self.players = [Player(self.cards,i+1) for i in range(NUM_PLAYERS)]

            self.current_player_index = -1
            self.next_player()
        else:
            with open(f'save_files/save_{save_file}.json') as file:
                data = json.load(file)
                self.supply = data['supply']
                self.players = [Player(self.cards,player['name'],basis=player) for player in data['players']]
                self.current_player_index = data['current_player_index']
                self.current_player = self.players[self.current_player_index]
                self.current_player.load_current_player_stats(data['current_player_stats'])


    def next_player(self):
        if self.current_player_index == len(self.players) - 1:
            self.current_player_index = 0
        else:
            self.current_player_index += 1
        self.current_player = self.players[self.current_player_index]
        self.current_player.start_turn()
        self.event_handler.reset()
        
    def run_menu_screen(self):
        '''Returns -1 if the player exited the program. Otherwise, returns the index of their choice.'''
        while True:
            self.ui.draw_background()
            self.ui.draw_menu(self.options)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    for i,option in enumerate(self.options):
                        if option.rect.collidepoint(mouse):
                            return i
    def run_game(self):
        while True:
            # Draw the background image
            self.ui.draw_background()
            # Handle events
            if self.event_handler.handle_events() == False:
                return
            # Draw Supply Stacks and Player Hand
            self.ui.draw_cards()
            # Draw the GUI
            self.ui.draw_gui()

            # Update the display
            pygame.display.flip()

if __name__ == "__main__":
    Master()
