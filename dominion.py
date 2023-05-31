import pygame
import random
import io
import json
import urllib.request
# https://www.ultraboardgames.com/dominion/gfx/<card_name>.jpg
# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CARD_WIDTH = 100
CARD_HEIGHT = 150
CARD_MARGIN = 10
GRAY = (200, 200, 200)

# Initialize pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dominion")

# Define Dominion card class
class DominionCard:
    def __init__(self, name, cost, type):
        self.name = name
        self.cost = cost
        self.type = type
        self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)
        self.image = self.load_image()

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

    def draw(self, surface, x, y):
        self.rect.topleft = (x, y)
        surface.blit(self.image, self.rect)

# Define Player class
class Player:
    def __init__(self):
        self.deck = []
        self.hand = []
        self.discard_pile = []
        self.initialize_deck()

    def initialize_deck(self):
        # Add starting cards to the deck
        starting_deck = ["Copper"] * 7 + ["Estate"] * 3
        self.deck = [DominionCard(card_name, 0, "") for card_name in starting_deck]
        random.shuffle(self.deck)

    def draw_cards(self, num_cards):
        # Draw a specified number of cards from the deck
        for _ in range(num_cards):
            if len(self.deck) == 0:
                # If the deck is empty, shuffle the discard pile and add it to the deck
                self.deck = self.discard_pile
                self.discard_pile = []
                random.shuffle(self.deck)
            if len(self.deck) > 0:
                card = self.deck.pop()
                self.hand.append(card)

    def draw_card(self, card):
        # Add a card to the player's hand
        self.hand.append(card)

# Initialize game objects
num_players = 2
players = [Player() for _ in range(num_players)]

cards = []
# cards = [
#     DominionCard("Copper", 0, "Treasure"),
#     DominionCard("Silver", 3, "Treasure"),
#     DominionCard("Gold", 6, "Treasure"),
#     DominionCard("Estate", 2, "Victory"),
#     DominionCard("Duchy", 5, "Victory"),
#     DominionCard("Province", 8, "Victory")
#     # Add more cards...
# ]
with open('assets/cards.json') as file:
    cards_file = json.load(file)
    for card in cards_file['Dominion']:
        print(card['name'])
        cards.append(DominionCard(card['name'],card['cost_treasure'],card['type']))


supply = {
    cards[0]: 60,  # Copper
    cards[1]: 40,  # Silver
    cards[2]: 30,  # Gold
    cards[3]: 8,   # Estate
    cards[4]: 8,   # Duchy
    cards[5]: 8    # Province
    # Add more cards...
}

# Load background image
background_image = pygame.image.load("./assets/background.jpg")
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Game loop
running = True
current_player_index = 0  # Set the initial current player index

while running:
    # Draw the background image
    window.blit(background_image, (0, 0))

    # Starting turn
    current_player = players[current_player_index]
    current_player.draw_cards(5)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                # Check if the player clicked on a supply stack
                for card in supply.keys():
                    if card.rect.collidepoint(mouse_pos):
                        # Draw a card from the selected supply pile
                        if supply[card] > 0:
                            current_player.draw_card(card)
                            supply[card] -= 1

    # # Clear the screen
    # window.fill(GRAY)

    # Draw supply stacks
    supply_x = WINDOW_WIDTH - CARD_MARGIN - CARD_WIDTH
    supply_y = CARD_MARGIN
    for i, card in enumerate(supply):
        card.draw(window, supply_x, supply_y + i * (CARD_HEIGHT + CARD_MARGIN))

    # Draw player hands
    for i, player in enumerate(players):
        for j, card in enumerate(player.hand):
            card_x = CARD_MARGIN + (CARD_WIDTH + CARD_MARGIN) * j
            card_y = WINDOW_HEIGHT - CARD_MARGIN - CARD_HEIGHT - (CARD_HEIGHT + CARD_MARGIN) * i
            card.draw(window, card_x, card_y)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
