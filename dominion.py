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
HIGHLIGHT_COLOR = (255, 255, 0)  # Yellow
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
GRAY = (200, 200, 200)
CARD_WIDTH = 100
CARD_HEIGHT = 150
CARD_MARGIN = 10
DEBUG = True

# GUI Constants
ACTIONS_GUI_IMAGE_PATH = "assets/gui_circle.png"
BUYS_GUI_IMAGE_PATH = "assets/gui_circle.png"
TREASURE_GUI_IMAGE_PATH = "assets/gui_circle.png"
GUI_SCROLL_IMAGE_PATH = "assets/gui_scroll.png"
GUI_IMAGE_SIZE = (40, 40)
SCROLL_IMAGE_SIZE = (40, 25)
GUI_IMAGE_MARGIN = 20
GUI_CORNER_OFFSET = 10
GUI_NUMBER_FONT_SIZE = 24
GUI_NUMBER_FONT_COLOR = (255, 255, 255)
LABEL_FONT_SIZE = 10
LABEL_FONT_COLOR = (0, 0, 0)

# Font settings
FONT_SIZE = 24
FONT_COLOR = (255, 255, 255)
FONT_PATH = pygame.font.match_font("arial")

# Initialize pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dominion")

def draw_gui(player):
    # Load GUI images
    actions_gui_image = pygame.image.load(ACTIONS_GUI_IMAGE_PATH).convert_alpha()
    buys_gui_image = pygame.image.load(BUYS_GUI_IMAGE_PATH).convert_alpha()
    treasure_gui_image = pygame.image.load(TREASURE_GUI_IMAGE_PATH).convert_alpha()
    gui_scroll_image = pygame.image.load(GUI_SCROLL_IMAGE_PATH).convert_alpha()

    # Scale down the GUI images
    actions_gui_image = pygame.transform.scale(actions_gui_image, GUI_IMAGE_SIZE)
    buys_gui_image = pygame.transform.scale(buys_gui_image, GUI_IMAGE_SIZE)
    treasure_gui_image = pygame.transform.scale(treasure_gui_image, GUI_IMAGE_SIZE)
    gui_scroll_image = pygame.transform.scale(gui_scroll_image, SCROLL_IMAGE_SIZE)

    # Calculate the positions of the GUI elements
    actions_pos = (WINDOW_WIDTH - GUI_CORNER_OFFSET - actions_gui_image.get_width(),
                   WINDOW_HEIGHT - GUI_CORNER_OFFSET - actions_gui_image.get_height())
    buys_pos = (actions_pos[0], actions_pos[1] - actions_gui_image.get_height() - GUI_IMAGE_MARGIN)
    treasure_pos = (buys_pos[0] - buys_gui_image.get_width() - GUI_IMAGE_MARGIN,
                    actions_pos[1])

    # Calculate the position of the scroll image
    scroll_pos_actions = (actions_pos[0],
                          actions_pos[1] - gui_scroll_image.get_height()/2)
    scroll_pos_buys = (buys_pos[0],
                       buys_pos[1] - gui_scroll_image.get_height()/2)
    scroll_pos_treasure = (treasure_pos[0],
                           treasure_pos[1] - gui_scroll_image.get_height()/2)

    # Draw the GUI images on the screen
    window.blit(actions_gui_image, actions_pos)
    window.blit(buys_gui_image, buys_pos)
    window.blit(treasure_gui_image, treasure_pos)

    # Draw the scroll images on the screen
    window.blit(gui_scroll_image, scroll_pos_actions)
    window.blit(gui_scroll_image, scroll_pos_buys)
    window.blit(gui_scroll_image, scroll_pos_treasure)

    # Render text surfaces
    font = pygame.font.Font(FONT_PATH, LABEL_FONT_SIZE)
    actions_label = font.render("Actions", True, LABEL_FONT_COLOR)
    buys_label = font.render("Buys", True, LABEL_FONT_COLOR)
    treasure_label = font.render("Treasure", True, LABEL_FONT_COLOR)

    # Position the text surfaces on the scrolls
    actions_label_pos = (scroll_pos_actions[0] + gui_scroll_image.get_width() // 2 - actions_label.get_width() // 2,
                         scroll_pos_actions[1] + gui_scroll_image.get_height() // 2 - actions_label.get_height() // 2)
    buys_label_pos = (scroll_pos_buys[0] + gui_scroll_image.get_width() // 2 - buys_label.get_width() // 2,
                      scroll_pos_buys[1] + gui_scroll_image.get_height() // 2 - buys_label.get_height() // 2)
    treasure_label_pos = (scroll_pos_treasure[0] + gui_scroll_image.get_width() // 2 - treasure_label.get_width() // 2,
                          scroll_pos_treasure[1] + gui_scroll_image.get_height() // 2 - treasure_label.get_height() // 2)

    # Draw the labels on the scrolls
    window.blit(actions_label, actions_label_pos)
    window.blit(buys_label, buys_label_pos)
    window.blit(treasure_label, treasure_label_pos)

    # Render and display the GUI numbers
    font = pygame.font.Font(FONT_PATH, GUI_NUMBER_FONT_SIZE)
    actions_number = font.render(str(player.actions), True, GUI_NUMBER_FONT_COLOR)
    buys_number = font.render(str(player.buys), True, GUI_NUMBER_FONT_COLOR)
    treasure_number = font.render(str(player.treasure), True, GUI_NUMBER_FONT_COLOR)

    # Position the GUI numbers on the GUI images
    actions_number_pos = (actions_pos[0] + actions_gui_image.get_width() // 2 - actions_number.get_width() // 2,
                          actions_pos[1] + actions_gui_image.get_height() // 2 - actions_number.get_height() // 2)
    buys_number_pos = (buys_pos[0] + buys_gui_image.get_width() // 2 - buys_number.get_width() // 2,
                       buys_pos[1] + buys_gui_image.get_height() // 2 - buys_number.get_height() // 2)
    treasure_number_pos = (treasure_pos[0] + treasure_gui_image.get_width() // 2 - treasure_number.get_width() // 2,
                           treasure_pos[1] + treasure_gui_image.get_height() // 2 - treasure_number.get_height() // 2)

    # Draw the GUI numbers on the screen
    window.blit(actions_number, actions_number_pos)
    window.blit(buys_number, buys_number_pos)
    window.blit(treasure_number, treasure_number_pos)

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
        game_cards.append(cards[13])
        used_cards.append(cards[13])

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
                        card.card.play(current_player, players, cards)

        # Change cursor and highlight cards on hover
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            # Reset highlights
            for card in cards:
                card.highlighted = False

            # Check if hovering over player's hand cards
            for card in current_player.hand:
                if card.rect.collidepoint(mouse_pos):
                    card.highlighted = True
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    break
            # Check if hovering over supply decks
            else:
                supply_x = CARD_MARGIN
                supply_y = CARD_MARGIN
                for card_id in supply:
                    card = cards[card_id]
                    if card.rect.collidepoint(mouse_pos):
                        card.highlighted = True
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        break
                    supply_x += CARD_WIDTH + CARD_MARGIN
                    if supply_x + CARD_WIDTH > WINDOW_WIDTH:
                        supply_x = CARD_MARGIN
                        supply_y += CARD_MARGIN + CARD_HEIGHT
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                current_player.end_turn()
                current_player.start_turn()

    # Draw supply stacks with highlighting
    supply_x = CARD_MARGIN
    supply_y = CARD_MARGIN
    for i, card_id in enumerate(supply):
        card = cards[card_id]
        if card.highlighted:
            pygame.draw.rect(window, HIGHLIGHT_COLOR, card.rect, 3)
        card.draw_stack(window, supply_x, supply_y)
        supply_x += CARD_WIDTH + CARD_MARGIN
        if supply_x + CARD_WIDTH > WINDOW_WIDTH:
            supply_x = CARD_MARGIN
            supply_y += CARD_MARGIN + CARD_HEIGHT

    # Draw player hand with highlighting
    for i, card in enumerate(current_player.hand):
        card_x = CARD_MARGIN + (CARD_WIDTH + CARD_MARGIN) * i
        card_y = WINDOW_HEIGHT - CARD_MARGIN - CARD_HEIGHT
        if card.highlighted:
            pygame.draw.rect(window, HIGHLIGHT_COLOR, card.rect, 3)
        card.draw(window, card_x, card_y)

    # Draw the GUI
    draw_gui(current_player)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()