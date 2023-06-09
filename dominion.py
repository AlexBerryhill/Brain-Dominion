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

        self.file_data = self.get_save_data()

        self.save_slot = self.run_menu_screen()
        if self.save_slot != -1:
            self.cards = load_cards()
            self.event_handler = EventHandler(self)
            self.load_game(self.save_slot)
            self.game_options = [Option("End Turn",(WINDOW_WIDTH - 90,WINDOW_HEIGHT-30),15)]
            if not self.run_game(): # If the game was quit, not finished, then save the game.
                self.save_game()
            else:
                self.finish_game()

        pygame.quit()

    def finish_game(self):
        '''If the game is finished, display the winner and reset the save file'''
        winner,scores = self.get_winner()
        print(f"Player {winner + 1} won!")
        print("Scores:")
        for i,score in enumerate(scores):
            print(f"Player {i + 1}: {score}")


        self.file_data[self.save_slot] = {'empty':True}
        with open('save_files.json','w') as file:
            json.dump(self.file_data,file)
    
    def get_pile_score(self,pile):
        return sum([card.card.victory_points for card in pile if card.card.type == "Victory"])
    
    def garden_score(self,player):
        score = (len(player.deck)+len(player.hand)+len(player.discard_pile)) // 10
        num_gardens = sum([sum([1 for card in pile if card.card.id == 15]) for pile in [player.deck,player.hand,player.discard_pile]])
        # num_gardens = 0
        # for pile in [player.deck,player.hand,player.discard_pile]:
        #     num_gardens += sum([1 for card in pile if card.card.id == 15])
        return score * num_gardens
    
    def get_winner(self):
        scores = [sum(map(self.get_pile_score,[player.deck,player.hand,player.discard_pile])) + self.garden_score(player) for player in self.players]
        return scores.index(max(scores)),scores

    
    def get_save_data(self):
        try:
            with open('save_files.json','r') as file:
                return json.load(file) 
        except FileNotFoundError:
            # If the file was not found, create a new set of save slots
            with open('save_files.json','w') as file:
                file_data = [{'empty':True},{'empty':True},{'empty':True},{'empty':True}]
                json.dump(file_data,file)
                return file_data
    
    def create_options(self):
        options = []
        for i,game in enumerate(self.file_data):
            options.append(Option(f"Save {i + 1} {'(Empty)' if game['empty'] else ''}",(200,200 + 60 * i)))
        return options

    
    def save_game(self):
        
        saved_game = {
            "empty":False,
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
        self.file_data[self.save_slot] = saved_game

        with open('save_files.json','w') as file:
            json.dump(self.file_data,file)


    def load_game(self,save_slot):
        if self.file_data[save_slot]["empty"]:
            self.supply = setup_game_cards(self.cards)
            self.players = [Player(self.cards,i+1,self) for i in range(NUM_PLAYERS)]

            self.current_player_index = -1
            self.next_player()
        else:
            data = self.file_data[save_slot]
            self.supply = {}
            for key,value in data['supply'].items():
                self.supply[int(key)] = value
            self.players = [Player(self.cards,player['name'],self,basis=player) for player in data['players']]
            self.current_player_index = data['current_player_index']
            self.current_player = self.players[self.current_player_index]
            self.current_player.load_current_player_stats(data['current_player_stats'])


    def next_player(self):
        for card_id in self.supply.keys():
            if self.supply[card_id] < 1 and self.cards[card_id].enabled:
                self.cards[card_id].enabled = False
        if self.current_player_index == len(self.players) - 1:
            self.current_player_index = 0
        else:
            self.current_player_index += 1
        self.current_player = self.players[self.current_player_index]
        self.current_player.start_turn()
        self.event_handler.reset()
    
    def is_over(self):
        return len([x for x in self.cards[7:] if not x.enabled]) >= 3 or self.supply[5] == 0

        
    def run_menu_screen(self):
        '''Returns -1 if the player exited the program. Otherwise, returns the index of their choice.'''
        while True:
            self.ui.draw_background()
            options = self.create_options()
            self.ui.draw_menu(options)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    for i,option in enumerate(options):
                        if option.rect.collidepoint(mouse):
                            return i
    def run_game(self):
        while True:
            self.ui.draw_background()
            if self.event_handler.handle_events() == False:
                return False
            self.ui.draw_options(self.game_options)
            self.ui.draw_cards()
            self.ui.draw_gui()
            if self.is_over():
                return True

            # Update the display
            pygame.display.flip()

if __name__ == "__main__":
    Master()
