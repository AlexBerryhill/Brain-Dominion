import pygame
import random
import json
from card import Card
from treasure_card import Treasure_card
from kingdom_card import Kingdom_card
from victory_card import Victory_card
from player import Player

# https://www.ultraboardgames.com/dominion/gfx/<card_name>.jpg
# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
GRAY = (200, 200, 200)
CARD_WIDTH = 100
CARD_HEIGHT = 150
CARD_MARGIN = 10
DEBUG = True

# Initialize pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dominion")



def load_cards():
    '''Using the cards.json file, returns a list of all the cards in the dominion game as objects.'''
    cards = []
    with open('assets/cards.json') as file:
        cards_file = json.load(file)
        for card in cards_file['Dominion']:
            if card['type'] == 'Treasure':
                cards.append(Treasure_card(card['name'],card['cost'],card['worth'],card['id'],card['starting_amount']))
            elif card['type'] == 'Victory':
                cards.append(Victory_card(card['name'],card['cost'],card['victory_points'],card['id'],card['starting_amount']))
            else:
                cards.append(Kingdom_card(card['name'],card['cost'],card['description'],card['plus_actions'],card['plus_treasure'],card['plus_buys'],card['plus_cards'],card['is_attack'],card['is_reaction'],card['id'],card['special_action']))
    return cards

cards = load_cards()
def setup_game_cards():
    '''Pulls the cards from the card list needed for a game (all victory and treasure cards and 10 kingdom cards)
    Returns a dictionary of card id's and the amount of that card there is at the start. 
    '''
    game_cards = cards[:7]
    used_cards = [0]

    #TEMPORARY CODE FOR DEBUGGING NEW KINGDOM CARD CODE
    if DEBUG:
        game_cards.append(cards[8])
        used_cards.append(cards[8])

    for _ in range(10 if DEBUG else 11):
        card_i = 0
        while card_i in used_cards:
            card_i = random.randint(7,31) 
        game_cards.append(cards[card_i])
    
    supply = {}
    for card in game_cards:
        supply[card.id] = card.starting_amount
    return supply

supply = setup_game_cards()
num_players = 2
players = [Player(cards) for _ in range(num_players)]



# Load background image
background_image = pygame.image.load("./assets/background.jpg")
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Game loop
running = True
current_player_index = 0  # Set the initial current player index

# Starting turn
current_player = players[current_player_index]
current_player.start_turn()
while running:
    # Draw the background image
    window.blit(background_image, (0, 0))


    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                # Check if the player clicked on a supply stack
                for card_id in supply.keys():
                    card = cards[card_id]
                    if card.rect.collidepoint(mouse_pos):
                        # Draw a card from the selected supply pile
                        if supply[card_id] > 0:
                            current_player.buy_card(card)
                            supply[card_id] -= 1

                for card in current_player.hand:
                    if card.rect.collidepoint(mouse_pos):
                        card.card.play(current_player,players,cards)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                current_player.end_turn()
                current_player.start_turn()

    # # Clear the screen
    # window.fill(GRAY)

    # Draw supply stacks
    supply_x = CARD_MARGIN
    supply_y = CARD_MARGIN
    for i, card_id in enumerate(supply):
        cards[card_id].draw_stack(window, supply_x, supply_y)
        supply_x += CARD_WIDTH + CARD_MARGIN
        if supply_x + CARD_WIDTH > WINDOW_WIDTH:
            supply_x = CARD_MARGIN
            supply_y += CARD_MARGIN + CARD_HEIGHT

    # Draw player hand
    for i, card in enumerate(current_player.hand):
        card_x = CARD_MARGIN + (CARD_WIDTH + CARD_MARGIN) * i
        card_y = WINDOW_HEIGHT - CARD_MARGIN - CARD_HEIGHT
        card.draw(window, card_x, card_y)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
